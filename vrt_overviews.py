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

path_data = r'\\lb-server\LB-Projekte\fernerkundung\luftbild\he\flugzeug\2022\he_lverm\tdop\daten'
path_out = path_data
# naming scheme for tiles: bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber_x-wert_y-wert
    # For abbreviations open "\\lb-server\LB-Projekte\SGB4_InterneVerwaltung\EDV\KON-GEO\2024\vrt_benennung\vrt_benennung.txt"
    # x-wert und y-wert will be added later
tile_name = 'he_flugzeug_2022_he_lverm_tdop'
# naming scheme for vrt: bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber
    # similar to folder structure see "Z:\SGB4_InterneVerwaltung\EDV\KON-GEO\2024\neustrukturierung_laufwerk_fernerkundung\Übersicht_Neustrukturierung_Laufwerke_nach_BL_Trägersystem_Jahr_Gebiet_20240130.docx"

vrt_name = tile_name
out_srs = 25832


path_meta = os.path.join(os.path.dirname(path_data),"doku")
cog_folder = 'kacheln'
vrt_folder = 'vrt'
footprint_folder = 'kacheluebersicht'

dir_cog = os.path.join(path_out,cog_folder)
dir_vrt = os.path.join(path_out,vrt_folder)
dir_footprint = os.path.join(path_out,footprint_folder)

#get all cog-tiles
dir_cog = pathlib.Path(dir_cog)
input_windows_path = dir_cog.rglob("*.tif")
tif = []
for x in input_windows_path:
    tif.append(str(x))
tile_sample = tif[0]
tif= '\n'.join(tif)

input_list_txt = os.path.join(dir_vrt, 'input_list.txt')
with open(input_list_txt, 'w') as file:
    file.write(tif)
    file.close()
vrt = os.path.join(path_data, vrt_name + '.vrt')
buildvrtString = 'gdalbuildvrt -overwrite -input_file_list '+ input_list_txt + ' ' + vrt
subprocess.run(buildvrtString)

level = [16, 2, 2, 2, 2, 2]
ovr_list = []

for x in level:
    if x == level[0]:
        gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' ' + str(x)
        print(gdaladdoString)
        subprocess.run(gdaladdoString)
        OVERVIEW_FILE = vrt+'.ovr'
        ovr_list.append(OVERVIEW_FILE)
        time_level = time.time()
    else:
        gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES --config OVERVIEW_COMPRESS ZSTD ' + OVERVIEW_FILE + ' ' + str(x)
        print(gdaladdoString)
        subprocess.run(gdaladdoString)
        OVERVIEW_FILE = OVERVIEW_FILE+'.ovr'
        ovr_list.append(OVERVIEW_FILE)
        time_level = time.time()
ovr_tif =[]

for x in ovr_list:
    x_split = x.split('.vrt.ovr')
    new_name =  x_split[0]+'2.tif'+x_split[1]
    os.rename(x, new_name)
    ovr_tif.append(new_name)
    os.rename(new_name, x)

vrt_ds = gdal.Open(vrt)
ulx, xres, xskew, uly, yskew, yres  = vrt_ds.GetGeoTransform()

ovr = ovr_tif[0]
ds = gdal.Open(ovr)
ds.SetProjection('EPSG:'+str(out_srs))
ds.SetGeoTransform([ulx, level[0]*xres, 0, uly, 0, level[0]*yres])
ds = None
gdaltransString = 'gdal_translate ' + ovr + ' ' + vrt[:-4]+ '.tif' + ' -co COMPRESS=ZSTD -co BIGTIFF=YES -co COPY_SRC_OVERVIEWS=YES --config OVERVIEW_COMPRESS ZSTD --config GDAL_NUM_THREADS ALL_CPUS' 
subprocess.run(gdaltransString)
ovr_final = vrt[:-4]+'.vrt.ovr'
os.rename(vrt[:-4]+ '.tif',ovr_final)

for x in ovr_tif:
    os.remove(x)
    os.remove(input_list_txt)