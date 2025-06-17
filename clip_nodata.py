import os
from osgeo import gdal, osr, ogr
import numpy as np
import subprocess
import time

input_path = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\ni\flugzeug\2009\harz_np\dop\daten"
nodata_value = 0

def clip_nodata(input, nodata_value):
    input_path = os.path.dirname(input)
    input_name = os.path.basename(input)
    mask_tif = os.path.join(input_path, f"{input_name.split('.')[0]}_mask{input_name.split('.')[1]}")
    cutline = os.path.join(input_path,f"{input_name.split('.')[0]}_cutline.gpkg")
    rename = os.path.join(input_path, f"{input_name.split('.')[0]}_rename{input_name.split('.')[1]}")
    os.rename(input, rename)

    dataset = gdal.Open(rename)
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
    dataset = None
    
    gdalcontour_String = f'gdal_contour -p -fl 1 -b 1 -f "GPKG" {mask_tif} {cutline}'
    print(gdalcontour_String)
    subprocess.run(gdalcontour_String)

    if {input_name.split('.')[1]} == 'tif':
        gdalwarpString = f"gdalwarp -overwrite -of COG -co COMPRESS=ZSTD -co PREDICTOR=2 -co BIGTIFF=YES --config OVERVIEW_COMPRESS ZSTD -co OVERVIEW_PREDICTOR=2 -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50  -cutline {cutline} -cl contour -crop_to_cutline {rename} {input}"
        subprocess.run(gdalwarpString)
    if {input_name.split('.')[-1]} == 'ovr':
    else:
    os.remove(mask_tif)
    os.remove(cutline)
    os.remove(rename)

clip_nodata(input_path, 0)

