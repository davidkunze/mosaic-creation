import os
from osgeo import gdal, osr, ogr
import numpy as np
import subprocess
import time
import pathlib
import multiprocessing as mp

# Parameters
path_data = r"\\lb-srv\LB-Z-Temp\David\vrt_cog\testdaten\test_nodata_clip\dop\daten"
nodata_value = 0
folder_exception = ['kacheln']  # Set to None or '' to disable filtering
formats = ['*.tif', '*.jpg', '*.png', '*.img', '*.ovr'] # Specify the formats to collect # If you want to collect all files, set it None
vrt_data = r"\\lb-srv\LB-Z-Temp\David\vrt_cog\testdaten\test_nodata_clip\dop\daten\kacheln"

# Function to collect files based on specified formats and exceptions
def collect_files(path, folder_exception=None, formats=None):
    path = pathlib.Path(path)
    if formats is None:
        formats = ['*']  # Match all files if no formats are specified
    collected_files = []
    for pattern in formats:
        for file_path in path.rglob(pattern):
            if folder_exception and any(exc in file_path.parent.as_posix() for exc in folder_exception):
                continue
            collected_files.append(str(file_path))
    
    return collected_files

# Function to clip nodata values from raster files
def clip_nodata(input, nodata_value, vrt_data_path):
    input_path = os.path.dirname(input)
    input_name = os.path.basename(input)
    mask_tif = os.path.join(input_path, f"{input_name.split('.')[0]}_mask.{input_name.split('.')[-1]}")
    cutline = os.path.join(input_path,f"{input_name.split('.')[0]}_cutline.gpkg")
    rename = os.path.join(input_path, f"{input_name.split('.')[0]}_rename.{input_name.split('.')[-1]}")
    os.rename(input, rename)

    if input.endswith('.ovr'):
        base_file = f"{input.split('.')[0]}.{input.split('.')[1]}"
        dataset = gdal.Open(base_file) # Open the base file of overview to read the geotransform and projection
        # if basefile.endswith('.vrt') and vrt_data_path:
        #     vrt_files = collect_files(vrt_data_path, formats=['*.tif', '*.jpg', '*.png', '*.img'])
        #     input_data_str = '\n'.join(vrt_files)
        #     input_list_txt = base_file.replace('.vrt', 'input_list.txt')
        #     with open(input_list_txt, 'w') as file:
        #         file.write(input_data_str)
        #         file.close()
        #     gdalBuildVRTString = f'gdalbuildvrt -overwrite -input_file_list {rename} {base_file}'
        #     subprocess.run(gdalBuildVRTString)
        #     remove_file = input_list_txt
    else:
        dataset = gdal.Open(rename)
    
    # Create a mask for nodata values across all bands
    band_count = dataset.RasterCount
    driver = gdal.GetDriverByName("GTiff")
    
    out_ds = driver.Create(
        mask_tif,
        dataset.RasterXSize,
        dataset.RasterYSize,
        1,
        gdal.GDT_Byte,
        options=["TILED=YES", "COMPRESS=DEFLATE"]
    )
    out_ds.SetGeoTransform(dataset.GetGeoTransform())
    out_ds.SetProjection(dataset.GetProjection())

    # Read nodata values and create a mask
    block_size = 1024

    for y in range(0, dataset.RasterYSize, block_size):
        rows = min(block_size, dataset.RasterYSize - y)
        for x in range(0, dataset.RasterXSize, block_size):
            cols = min(block_size, dataset.RasterXSize - x)
            band_list = []
            for band in range(1, band_count + 1):
                b = dataset.GetRasterBand(band).ReadAsArray(x, y, cols, rows)
                band_list.append(b == nodata_value)
            mask = np.logical_and.reduce(band_list).astype(np.uint8)
            out_ds.GetRasterBand(1).WriteArray(mask, x, y)
    out_ds.GetRasterBand(1).SetNoDataValue(1)
    out_ds = None
    
    # Create a cutline from the mask
    gdalpolygonizeString = f'gdal_polygonize {mask_tif}  -b 1 -f "GPKG" {cutline} outline'
    subprocess.run(gdalpolygonizeString)
    # gdalcontour_String = f'gdal_contour -p -fl 1 -b 1 -nln outline -f "GPKG" {mask_tif} {cutline}'
    # subprocess.run(gdalcontour_String)
    
    # Clip the input raster using the cutline
    if input.endswith('.tif'):
        gdalwarpString = f"gdalwarp -overwrite -r rms -of COG -dstnodata None -co COMPRESS=ZSTD -co PREDICTOR=2 -co BIGTIFF=YES --config OVERVIEW_COMPRESS ZSTD -co OVERVIEW_PREDICTOR=2 -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50  -cutline {cutline} -cl outline -crop_to_cutline {rename} {input}"
        subprocess.run(gdalwarpString)
    if input.endswith('.ovr'):
        rename_ds = gdal.Open(rename) # Open the ovr dataset to set positional parameter to achieve correct positioning
        xres_rename = rename_ds.GetGeoTransform()[1] # Get the x resolution from the ovr dataset
        yres_rename = rename_ds.GetGeoTransform()[5] # Get the y resolution from the ovr dataset  
        rename_ds.SetGeoTransform(dataset.GetGeoTransform()) # Set the geotransform from the base dataset
        ulx, xres, xskew, uly, yskew, yres = dataset.GetGeoTransform() # Get the geotransform from the base dataset
        rename_ds.SetGeoTransform([ulx, xres_rename, 0, uly, 0, yres_rename]) #set the geotransform from the base dataset with the x and y resolution from the ovr dataset
        rename_ds.SetProjection(dataset.GetProjection()) # Set the projection from the base dataset
        rename_ds = None        
        tif = rename.replace('.ovr','.tif')
        # clip the ovr dataset with data specifications as output format and compression
        gdalwarpString = f"gdalwarp -overwrite -r rms -of COG -dstnodata None -co COMPRESS=ZSTD -co PREDICTOR=2 -co BIGTIFF=YES --config OVERVIEW_COMPRESS ZSTD -co OVERVIEW_PREDICTOR=2 -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50 -cutline {cutline} -cl outline -crop_to_cutline {rename} {tif}"
        print(gdalwarpString)
        subprocess.run(gdalwarpString)
        os.rename(tif, input)
    else:
        gdalwarpString = f"gdalwarp -overwrite -r rms -dstnodata None -co COMPRESS=ZSTD -co PREDICTOR=2 -co BIGTIFF=YES -cutline {cutline} -cl outline -crop_to_cutline {rename} {input}"
        subprocess.run(gdalwarpString)

    dataset = None

    os.remove(mask_tif)
    os.remove(cutline)
    os.remove(rename)

input_data = collect_files(path_data, folder_exception, formats)

if __name__ == '__main__':
    count = mp.cpu_count()
    pool = mp.Pool(count-count+4)
    args = [(x, nodata_value, vrt_data) for x in input_data]
    pool.starmap(clip_nodata, args)
    pool.close()
    pool.join()

print("Processing complete.")
