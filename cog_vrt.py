import os
import sys
from glob import glob
import pathlib
import multiprocessing as mp
import time
import fiona
from shapely.geometry import Point, LineString, Polygon
import geopandas
import pandas
import numpy
import subprocess
# import rasterio
# import rioxarray as rxr
from osgeo import gdal, osr, ogr
gdal.UseExceptions()

start_time = time.time()

path_data = r'Y:\David\vrt_cog\testdaten\lidar_solling_2023\daten'
path_out = path_data
# naming scheme for tiles: bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber_x-wert_y-wert
    # For abbreviations open "\\lb-server\LB-Projekte\SGB4_InterneVerwaltung\EDV\KON-GEO\2024\vrt_benennung\vrt_benennung.txt"
    # x-wert und y-wert will be added later
tile_name = 'ni_flugzeug_2023_solling_ndom_nlf'
# naming scheme for vrt: bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber
    # similar to folder structure see "Z:\SGB4_InterneVerwaltung\EDV\KON-GEO\2024\neustrukturierung_laufwerk_fernerkundung\Übersicht_Neustrukturierung_Laufwerke_nach_BL_Trägersystem_Jahr_Gebiet_20240130.docx"

vrt_name = tile_name
# fill string if special nodata-value such as "255" is used in data
nodata_value = '' 

out_srs = 25832 #EPSG-code of output projection

path_meta = os.path.join(os.path.dirname(path_data),"doku")
cog_folder = 'kacheln'
vrt_folder = 'vrt'
footprint_folder = 'kacheluebersicht'


#get all files from dictionary and subdictionary
formats = ('*.tif','*.jgp','*.png','*.img')
path_data = pathlib.Path(path_data)
input_windows_path = []
for x in formats:
    input_windows_path.extend(path_data.rglob(x))
#transform windows path to string
input_data = []
for x in input_windows_path:
    input_data.append(str(x))

# print(input_data)

#create subfolder
def create_folder(output_f, folder_name):
    if not os.path.isdir(os.path.join(output_f, folder_name)):
        os.mkdir(os.path.join(output_f, folder_name))

folder_list = [cog_folder, vrt_folder, footprint_folder]
for x in folder_list:
    create_folder(path_out,x)
dir_cog = os.path.join(path_out,cog_folder)
dir_vrt = os.path.join(path_out,vrt_folder)
dir_footprint = os.path.join(path_out,footprint_folder)

# create temporary vrt from raw data
vrt_temp = os.path.join(dir_vrt, 'temp.vrt')
input_data_str = ' '.join(input_data)
buildvrtString = 'gdalbuildvrt -overwrite ' + vrt_temp + ' ' + input_data_str
bat_file = os.path.join(dir_vrt, 'batch.bat')
with open(bat_file, 'w') as file:
    file.write(buildvrtString)
    file.close()
subprocess.run(bat_file)


gdalinfoStrng = 'gdalinfo '+vrt_temp
# subprocess.run(gdalinfoStrng)
folder_list.append(os.path.basename(vrt_temp))

### get metadata of the input data
vrt_temp_ds = gdal.Open(vrt_temp)
# get input data projection
proj = osr.SpatialReference(wkt=vrt_temp_ds.GetProjection())
in_srs = proj.GetAttrValue('AUTHORITY',1)

# get input data datatype
band = vrt_temp_ds.GetRasterBand(1)
dtype = gdal.GetDataTypeName(band.DataType)
# get count of raster bands to know which band is alpha raster
band_count = vrt_temp_ds.RasterCount
# get nodata value
if nodata_value == '':
    nodata_value = vrt_temp_ds.GetRasterBand(1).GetNoDataValue()
    # rxr_vrt = rxr.open_rasterio(vrt_temp)
    # rxr_vrt.rio.write_nodata(nodata_value, inplace=True)
else:
    i = 1
    nodata_list = []
    while i < band_count+1:
        nodata_list.append(nodata_value)
        i += 1
    buildvrtString = 'gdalbuildvrt -srcnodata "' + ' '.join(nodata_list) + '" -overwrite ' + vrt_temp + ' ' + input_data_str
    with open(bat_file, 'w') as file:
        file.write(buildvrtString)
        file.close()
    subprocess.run(bat_file)

# get input data extent to check which output tiles contain data
inputdata_extent = os.path.join(dir_vrt, 'inputdata_extent.gpkg') 
gdaltindexString = 'gdaltindex ' + inputdata_extent + ' ' + input_data_str
bat_file = os.path.join(dir_vrt, 'batch.bat')
with open(bat_file, 'w') as file:
    file.write(gdaltindexString)
    file.close()
subprocess.run(bat_file)

### reproject raw data if not EPSG: 25832
# function to check whether raw data is stored in subfolders
print('in_srs: ' + str(in_srs))
print('out_srs: ' +str(out_srs))
warning = ''
if not in_srs in [str(out_srs)]:
    vrt_temp_proj = os.path.join(dir_vrt, 'temp_'+str(out_srs)+'.vrt')
    gdalwarpString = 'gdalwarp -of VRT -t_srs EPSG:' + str(out_srs) + ' ' + vrt_temp + ' ' + vrt_temp_proj
    subprocess.run(gdalwarpString)
    # os.remove(vrt_temp)
    vrt_temp = vrt_temp_proj
    inputdata_extent_proj = os.path.join(dir_vrt, 'inputdata_extent_' + str(out_srs) + '.gpkg') 
    ogr2ogrString = 'ogr2ogr -a_srs EPSG:' + str(out_srs) + ' ' + inputdata_extent_proj + ' ' + inputdata_extent
    warning =  '\n\n\n\n\n WARNHINWEIS! Ausgangsdaten haben kein Koordinatensystem zugewiesen, bitte nachprüfen, ob Daten vollständig und lagerichtig berechnet wurden! \n\n\n\n\n'
    subprocess.run(ogr2ogrString)    
    os.remove(inputdata_extent)
    inputdata_extent = inputdata_extent_proj
dataframe = geopandas.read_file(inputdata_extent, layer='inputdata_extent')
dataframe = dataframe.dissolve(by=None)
dataframe.to_file(inputdata_extent, layer='inputdata_extent', driver="GPKG")

### tiling temporary vrt into cog tiles
# get extent, raster origin
vrt_temp_ds_2 = gdal.Open(vrt_temp)
ulx, xres, xskew, uly, yskew, yres  = vrt_temp_ds_2.GetGeoTransform()
print('ulx: ' + str(int(ulx)))

# tranform width and height from count of pixel into map unit (for epsg "25832": metre)
width = abs(int(vrt_temp_ds.RasterXSize*xres))
height = abs(int(vrt_temp_ds.RasterYSize*yres))
print('ulx_int+width: '+str(int(ulx+width)))
tilesize = 2000

# Convert height to a number with an even number of thousands
if (int(str(height)[:-3]) % 2) == 0:
    height = int(str(height)[:-3]+"000")+4000
else:
    height = int(str(height)[:-3]+"000")+3000

# Convert width to a number with an even number of thousands
print('width: ' + str(width))
if (int(str(width)[:-3]) % 2) == 0:
    width = int(str(width)[:-3]+"000")+4000
else:
    width = int(str(width)[:-3]+"000")+3000
print('width_int_add: ' + str(width))

# Convert ulx, uly to a number with an even number of thousands

ulx_int = int(str(int(ulx))[:-3]+"000")
if (int(str(ulx_int)[:-3]) % 2) == 0:
    ulx_int = int(str(ulx_int)[:-3]+"000")
else:
    ulx_int = int(str(ulx_int)[:-3]+"000")-1000
print('ulx_int: '+str(ulx_int))

uly_int = int(str(int(uly))[:-3]+"000")+tilesize
if (int(str(uly_int)[:-3]) % 2) == 0:
    uly_int = int(str(uly_int)[:-3]+"000")+2000
    height = height+2000
else:
    uly_int = int(str(uly_int)[:-3]+"000")+1000

tiles = []
tiles_polygon =[]
tiles_polygon_select =[]
tiles_all = []
# geotransform=[]

print('ulx_int+width: '+str(ulx_int+width))

# get tile extent for gdal translate
for i in range(ulx_int, ulx_int+width, tilesize):
    for j in range(uly_int-height, uly_int, tilesize):
        lrx = i+tilesize
        lry = j-tilesize
        tile_ext=[]
        tile_ext.append(i)
        tile_ext.append(j)
        tile_ext.append(lrx)
        tile_ext.append(lry)
        tiles_all.append(tile_ext)

# check if tile intersect with data outline
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(i, j)
        ring.AddPoint(i, lry)
        ring.AddPoint(lrx, lry)
        ring.AddPoint(lrx, j)
        ring.AddPoint(i, j)
        extentGeometry = ogr.Geometry(ogr.wkbPolygon)
        extentGeometry.AddGeometry(ring)
        vector = ogr.Open(inputdata_extent)
        layer = vector.GetLayer()
        feature = layer.GetFeature(1)
        vectorGeometry = feature.GetGeometryRef()
        
        polygon_points = []
        polygon_points.append([i, j])
        polygon_points.append([i, lry])
        polygon_points.append([lrx, lry])
        polygon_points.append([lrx, j])
        polygon_points.append([i, j])
        tiles_polygon.append(Polygon(polygon_points))
        if extentGeometry.Intersect(vectorGeometry) == True:
            tiles.append(tile_ext)
            tiles_polygon_select.append(Polygon(polygon_points))
        del vector
polygon=[]
for x in tiles_polygon:
    polygon.append(geopandas.GeoDataFrame(crs='epsg:'+str(out_srs), geometry=[x]))
df_polygons = pandas.concat(polygon)        
df_polygons.to_file(filename=os.path.join(dir_vrt,'polygon.gpkg'), driver="GPKG")
polygon=[]
for x in tiles_polygon_select:
    polygon.append(geopandas.GeoDataFrame(crs='epsg:'+str(out_srs), geometry=[x]))
df_polygons = pandas.concat(polygon)        
df_polygons.to_file(filename=os.path.join(dir_vrt,'polygon_select.gpkg'), driver="GPKG")
print('all tiles: ' + str(len(tiles_all)))
print('selected tiles: '+ str(len(tiles)))

 
def tiling(input, out_path, extent, count_bands, tile_size, x_res, y_res):
    i = 1
    bands = []
    while i < count_bands + 2:
        x = '-b ' + str(i)
        bands.append(x)
        i += 1
    # bands from raw data
    bands = ' '.join(bands[0:count_bands])
    output_name = tile_name+'_' +str(extent[0]) + "_" + str(extent[3])
    output = os.path.join(out_path, output_name + ".tif")
    
    # if tile size divided by raster resolution is float the raster cell size needs to be adjusted to prevent empty rows/column between tiles
    resamp_method ='nearest'
    cell_count_x = tile_size/x_res # number of pixels per row
    cell_count_y = tile_size/y_res # number of pixels per column
    if (cell_count_x).is_integer() == False or (cell_count_y).is_integer()== False:
        x1 = cell_count_x - int(cell_count_x) # get remaining pixel
        x2 = x1*x_res # get remainder in crs unit (e.g. metre)
        x3 = x2/int(cell_count_x) # remainder per pixel cell
        x_res = x_res + x3 # new cell size = original cell size + remainder per pixel cell
        y1 = cell_count_y - int(cell_count_y) # get remaining pixel
        y2 = y1*y_res # get remainder in crs unit (e.g. metre)
        y3 = y2/int(cell_count_y) # remainder per pixel cell
        y_res = y_res + y3 # new cell size = original cell size + remainder per pixel cell
        resamp_method = 'rms'

    # images will be compressed lossless with DEFLATE compression 
    # overviews of the 8-bit images can be created with the more space-saving JPEG compression
        # the overview compression method of 16-bit-images is DEFLATE
    if dtype == 'Byte':
        comp = 'JPEG'
    else:
        comp = 'DEFLATE'
    
    gdaltranString = 'gdal_translate -q -of COG -co COMPRESS=DEFLATE -co PREDICTOR=2 -r '+resamp_method+' -a_srs EPSG:' + str(out_srs) + ' ' + bands + ' -tr ' + str(x_res) + ' ' + str(y_res) + ' -co BIGTIFF=YES --config GDAL_TIFF_INTERNAL_MASK YES -co OVERVIEWS=IGNORE_EXISTING -co OVERVIEW_COMPRESS=' + comp + ' -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50 -projwin ' + str(extent[0]) + ', ' + str(extent[1]) + ', ' + str(extent[2]) + ', ' + str(extent[3]) + ' ' + input + ' ' + output
    subprocess.run(gdaltranString)
    # create polygon from data extent
    footprint = os.path.join(dir_footprint, output_name + ".gpkg")
    gdalvectorString = 'gdal_contour -q -fl 1 -b 1 -f "GPKG" -p ' + output + ' ' + footprint
    subprocess.run(gdalvectorString)


# ###############
# create 2x2 km cog tiles from vrt that was created from input data  
if __name__ == '__main__':
    count = mp.cpu_count()
    pool = mp.Pool(count-5)
    args = [(vrt_temp, dir_cog, x, band_count, tilesize, xres, yres) for x in tiles]
    pool.starmap(tiling, args)
    pool.close()

    # create extent vector layer which contains following three layers
    #   outline of complete dataset
    #   outline of each tile
    #   all 2x2 km tiles which contain data
    vector_data = glob(os.path.join(dir_footprint, '*000.gpkg'))
    tiles_valid = []
    for x in vector_data:
        df = geopandas.read_file(x, layer='contour')
        tif_path = os.path.join(dir_cog, os.path.basename(x)[:-5]+'.tif')
        # remove empty vector tiles, raster tiles
        if df.empty:
            os.remove(x)
            os.remove(tif_path)
        else:
            if 'path' not in df:
                df.insert(1, 'path', tif_path)
            tiles_valid.append(df)
    extent = os.path.join(dir_footprint, tile_name+'_extent.gpkg')

    # merge all tile outlines 
    df_merged = pandas.concat(tiles_valid)
    df_merged['geometry'] = df_merged['geometry'].make_valid().buffer(xres, join_style = 2).buffer(-1*xres, join_style = 2)
    df_merged = df_merged.dissolve(by='path')
    df_merged.to_file(extent, layer='footprint_outline', driver="GPKG")
    # dissolve tile outlines to dataset outline
    df_outline = df_merged.dissolve(by='ID')
    df_outline['geometry'] =df_outline['geometry'].make_valid().buffer(xres, join_style = 2).buffer(-1*xres, join_style = 2)
    df_outline.to_file(extent, layer='outline', driver="GPKG")
    # get all 2x2 km tiles which contain data
    gdalindex_string = 'gdaltindex -lyr_name footprints ' + extent + ' ' + os.path.join(dir_cog) + '/*.tif'
    subprocess.run(gdalindex_string)

    # read metadaten files
    metadata = glob(os.path.join(path_meta, '*.csv'))
    metadata = pandas.read_csv(metadata[0], sep='\r\n', skip_blank_lines=True, header=None, encoding='utf-8', engine='python')
    metadata = metadata.values.flatten().tolist()

    # add metadata to vector tiles
    def insert_medata(file):
        layers = fiona.listlayers(file)
        for table in layers:
            dataframe = geopandas.read_file(file, layer=table)
            for x in metadata:
                x = x.rstrip()
                if ';' in x:
                    y = x.split(';')
                    column = y[0]
                    value = y[1]
                    dataframe.insert(len(dataframe.columns), column, '') #add column to dataframe
                    dataframe[column] = value  #fill coulumn
            index = dataframe.columns.get_loc('datum_bildflug_von')
            dataframe.insert(index, 'bildflug_jahr', '')  # add column to dataframe
            dataframe['bildflug_jahr'] = dataframe['datum_bildflug_von'].str.split('-')[0][0]  # fill coulumn
            dataframe.loc[dataframe['epsg']!= str(out_srs),'epsg'] = str(out_srs)
            if 'ID' in dataframe.columns:
                dataframe.drop(['ID'],axis=1,inplace=True)
            dataframe.to_file(file, layer=table, driver="GPKG")

    insert_medata(extent)


    # build vrt from cog tiles
    dir_cog = pathlib.Path(dir_cog)
    input_windows_path = dir_cog.rglob("*.tif")
    tif = []
    for x in input_windows_path:
        tif.append(str(x))
    tile_sample = tif[1]
    tif= ' '.join(tif)

    vrt = os.path.join(dir_vrt, vrt_name+'.vrt')
    buildvrtString = 'gdalbuildvrt -overwrite '+vrt+' '+tif
    with open(bat_file, 'w') as file:
        file.write(buildvrtString)
        file.close()
    subprocess.run(bat_file)

    # create vrt overviews
    tile_sample = gdal.Open(tile_sample)
    tile_sample_band = tile_sample.GetRasterBand(1)
    tile_sample_band.GetOverviewCount
    # tile_sample_overview = tile_sample_band.GetOverview(3)
    # arr1 = tile_sample_overview.ReadAsArray()
    for x in tile_sample.GetMetadata():
        print(x)
    dir(tile_sample.GetDescription())
    
    # gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config BIGTIFF IF_SAFER -minsize 128 --config OVERVIEW_COMPRESS ZSTD ' + vrt
    gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES  --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' 16 32 64 128 256 512'
    subprocess.run(gdaladdoString)

    # remove temporary layers
    vector_list = glob(os.path.join(dir_footprint, '*'))
    for x in vector_list:
        if x != extent:
            os.remove(x)

    vector_list = glob(os.path.join(dir_vrt, '*'))
    for x in vector_list:
        if not os.path.basename(x).startswith(vrt_name):
            openfile = open(x)
            openfile.close()
            print(x)
            os.remove(x)

    hours, rem = divmod(time.time() - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    if warning != '':
        print(warning)
