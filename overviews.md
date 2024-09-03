|method|levels|processing time|perfomance qgis|perfomance arcgis|problems|
|---|---|---|---|---|---|
|gdaladdo: all levels in one command|very slow|16 to 512|good|good|additional storage needed due to smaller overview levels|
|gdaladdo: all levels in one command|very slow|128 to 512|good|smaller levels bad, can probably not read overview from cog||
|gdaladdo: one command per level|slow|16 to 512|good|good|many .ovr, merging still problem|
|rasterio: buildoverviews: all levels in one command|very slow, similar to gdaladdo|16 to 512|good|good|no advantage to gdaladdio|

# gdaladdo: all levels in one command (16 to 512)
gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES  --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' 16 32 64 128 256 512'
subprocess.run(gdaladdoString)

# gdaladdo: all levels in one command (128 to 512)
gdaladdoString = 'gdaladdo -r average -ro --config GDAL_NUM_THREADS ALL_CPUS --config COPY_SRC_OVERVIEWS YES  --config OVERVIEW_COMPRESS ZSTD ' + vrt + ' 128 256 512'
subprocess.run(gdaladdoString)

# gdaladdo: one command per level (16 to 512)
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
