Umcompressed images are tifs, compressed imags are Cloud Optimized Geotiff including internal overviews

|bit-depth|compression|predictor|level|time_write (s)|time_read (s)|size (MB)|
|---|---|---|---|---|---|---|
|8|uncompressed||||00.53|409.604|
|8|ZSTD|2|1|13.69|3.20|367.617|
|8|ZSTD|2|9 (default)|26.07|3.16|332.581|
|8|ZSTD|2|22|276.06|3.82|304.976|
|8|DEFLATE|2|1|16.42|3.09|363.483|
|8|DEFLATE|2|6 (default)|23.04|3.51|332.143|
|8|DEFLATE|2|9|24.76|3.71|332.143|
|16|uncompressed||||1.18|819.204|
|16|ZSTD|2|1|29.80|7.65|958.117|
|16|ZSTD|2|9 (default)|33.23|7.48|958,040|
|16|ZSTD|2|22|325.24|7.89|958,290|
|16|DEFLATE|2|1|30.06|7.33|958.333|
|16|DEFLATE|2|6 (default)|34.85|7.44|958.324|
|16|DEFLATE|2|9|34.95|7.88|958.324|


code used for testing
```python 
import os
import time
from osgeo import gdal, osr, ogr
import subprocess

start_time = time.time()

# input = r"\\lb-server\LB-Z-Temp\David\vrt_cog\testdaten\compression\596000_5730000_8bit.tif"
input = r"\\lb-server\LB-Z-Temp\David\vrt_cog\testdaten\compression\596000_5730000_16bit.tif"

comp = 'DEFLATE'
comp_level = 1
resamp_method = 'rms'
out_srs='25832'

output = os.path.join(os.path.dirname(input), os.path.basename(input[:-4])+'_'+comp+'_lev'+str(comp_level)+'.tif')

gdaltranString ='gdal_translate -q -of COG -co COMPRESS=ZSTD -co PREDICTOR=2 -co LEVEL='+str(comp_level)+' -r '+resamp_method+' -a_srs EPSG:' + str(out_srs) + ' ' + ' -co BIGTIFF=IF_NEEDED --config GDAL_TIFF_INTERNAL_MASK YES -co OVERVIEWS=IGNORE_EXISTING -co OVERVIEW_COMPRESS=' + comp + ' -co OVERVIEW_PREDICTOR=2 -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50 '+ ' ' + input + ' ' + output
# gdaltranString ='gdal_translate -q -of COG -co COMPRESS=ZSTD -co PREDICTOR=2 -r '+resamp_method+' -a_srs EPSG:' + str(out_srs) + ' ' + ' -co BIGTIFF=IF_NEEDED --config GDAL_TIFF_INTERNAL_MASK YES -co OVERVIEWS=IGNORE_EXISTING -co OVERVIEW_COMPRESS=' + comp + ' -co OVERVIEW_PREDICTOR=2 -co OVERVIEW_RESAMPLING=average -co OVERVIEW_QUALITY=50 '+ ' ' + input + ' ' + output
subprocess.run(gdaltranString)

hours, rem = divmod(time.time() - start_time, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
```
