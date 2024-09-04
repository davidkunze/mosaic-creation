Create overviews --> tested with Solling data from 2023

|method|levels|processing time|perfomance qgis|perfomance arcgis|problems|
|---|---|---|---|---|---|
|gdaladdo: all levels in one command|very slow (ca. 23 h)|16 to 512|good|good|additional storage needed due to smaller overview levels|
|gdaladdo: all levels in one command|very slow|128 to 512|good|smaller levels very slow, arcgis probably can not read overview from cog||
|gdaladdo: one command per level|slow (ca. 19 h)|16 to 512|good|good|several ovr-files, merging still problem|
|rasterio: buildoverviews: all levels in one command|very slow, similar to gdaladdo (ca. 23 h)|16 to 512|good|good|no advantage to gdaladdo|

# gdaladdo: all levels in one command (16 to 512)
```python
gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES  --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' 16 32 64 128 256 512'
subprocess.run(gdaladdoString)
```
# gdaladdo: all levels in one command (128 to 512)
```python
gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES  --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' 128 256 512'
subprocess.run(gdaladdoString)
```
# gdaladdo: one command per level (16 to 512)
```python
level = [16, 2, 2, 2, 2, 2]
OVERVIEW_FILE = vrt_temp_2+'.ovr'
ovr_list = []

for x in level:
    if x == level[0]:
        gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES --config OVERVIEW_COMPRESS ZSTD ' + vrt_temp_2 + ' ' + str(x)
        print(gdaladdoString)
        subprocess.run(gdaladdoString)
        ovr_list.append(OVERVIEW_FILE)
        time_level = time.time()
    else:
        gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES --config OVERVIEW_COMPRESS ZSTD ' + OVERVIEW_FILE + ' ' + str(x)
        print(gdaladdoString)
        subprocess.run(gdaladdoString)
        OVERVIEW_FILE = OVERVIEW_FILE
        ovr_list.append(OVERVIEW_FILE)
        time_level = time.time()
```
Merging method 1:
- gdal_merge:
- issue: result not readable
```python
over_merge = vrt[:-4]+'.tif'
gdal_merge_string = 'gdal_merge -of gtiff --config GDAL_NUM_THREADS ALL_CPUS -o ' + over_merge + ' ' + ' '.join(ovr_list)
print(gdal_merge_string)
subprocess.run(gdal_merge_string)
```

Merging method 2:
- create empty vrt with the extent of input data
- empty vrt is named like ovr-files and can recognise the ovr-files as overviews
- translate vrt with the option "-co COPY_SRC_OVERVIEWS=YES" to tif
- rename .tif to .vrt.ovr
```python
vrt_temp_ds = gdal.Open(vrt_temp)
proj = osr.SpatialReference(wkt=vrt_temp_ds.GetProjection())
in_srs = proj.GetAttrValue('AUTHORITY',1)
band_count = vrt_temp_ds.RasterCount
band = vrt_temp_ds.GetRasterBand(1)
dtype = band.DataType
ulx, xres, xskew, uly, yskew, yres  = vrt_temp_ds.GetGeoTransform()
width = abs(int(vrt_temp_ds.RasterXSize))
height = abs(int(vrt_temp_ds.RasterYSize))
driver = gdal.GetDriverByName('vrt')
vrt_temp_ds = None
os.remove(vrt_temp)

liste =[vrt_temp, width, height, band_count, dtype]
for x in liste:
    print(x)

ds = driver.Create(vrt_temp, width, height, band_count, dtype)
ds.SetProjection('EPSG:'+in_srs)
nodata_value = 65535
ds.SetGeoTransform([ulx, xres, 0, uly, 0, yres])
x = 1
while x <= band_count:
    ds.GetRasterBand(x).SetNoDataValue(nodata_value)
    print(x)
    x+=1
ds = None

gdaltransString = 'gdal_translate ' + vrt_temp + ' ' + vrt[:-4]+ '.tif' + ' -co COMPRESS=ZSTD -co BIGTIFF=YES -co COPY_SRC_OVERVIEWS=YES --config OVERVIEW_COMPRESS ZSTD --config GDAL_NUM_THREADS ALL_CPUS' 
subprocess.run(gdaltransString)
```
# rasterrio: buildoverviews (16 to 512)
```python
factors = [16, 32, 64, 128, 256, 512]
dst = rasterio.open(vrt)
dst.build_overviews(factors, Resampling.average)
dst.update_tags(ns='rio_overview', resampling='average')
dst.close()
```
