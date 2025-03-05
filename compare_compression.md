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


code used for creating files
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
code used for reading files
```python 
import os
import time
import pathlib
from osgeo import gdal, osr, ogr
import subprocess

path_data = r"\\lb-server\LB-Z-Temp\David\vrt_cog\testdaten\compression"
formats = ['*.tif']
path_data = pathlib.Path(path_data)
input_windows_path = []
for x in formats:
    input_windows_path.extend(path_data.rglob(x))
#transform windows path to string
input_data = []
for x in input_windows_path:
    input_data.append(str(x))

for x in input_data:
    start_time = time.time()
    ds = gdal.Open(x).ReadAsArray()
    hours, rem = divmod(time.time() - start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(x+': '+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
```

# Compression Performance Comparison

| Input File | Method   | Predictor | Level         | Type     | Size (MB) | Write Time (s) | Read Time (s) |
|------------|----------|-----------|--------------|----------|----------|----------------|---------------|
| 547000_5725000.tif | uncompressed | N/A       | N/A          | N/A      | 1560.35  | N/A            | 6.601         |
| 547000_5725000.tif | LZW      | 1         | N/A          | Lossless | 1094.56  | 14.34          | 5.415         |
| 547000_5725000.tif | LZW      | 2         | N/A          | Lossless | 569.08   | 15.98          | 5.044         |
| 547000_5725000.tif | DEFLATE  | 1         | 1            | Lossless | 891.47   | 11.3           | 2.883         |
| 547000_5725000.tif | DEFLATE  | 1         | 6 (Default)  | Lossless | 846.27   | 16.57          | 3.235         |
| 547000_5725000.tif | DEFLATE  | 1         | 9            | Lossless | 839.33   | 43.68          | 3.237         |
| 547000_5725000.tif | DEFLATE  | 2         | 1            | Lossless | 539.42   | 9.453          | 3.021         |
| 547000_5725000.tif | DEFLATE  | 2         | 6 (Default)  | Lossless | 525.70   | 29.23          | 3.026         |
| 547000_5725000.tif | DEFLATE  | 2         | 9            | Lossless | 504.88   | 100.8          | 3.06          |
| 547000_5725000.tif | ZSTD     | 1         | 1            | Lossless | 913.23   | 17.87          | 1.989         |
| 547000_5725000.tif | ZSTD     | 1         | 9 (Default)  | Lossless | 913.23   | 18.18          | 2.006         |
| 547000_5725000.tif | ZSTD     | 1         | 22           | Lossless | 913.23   | 17.82          | 1.99          |
| 547000_5725000.tif | ZSTD     | 2         | 1            | Lossless | 541.00   | 27.12          | 2.917         |
| 547000_5725000.tif | ZSTD     | 2         | 9 (Default)  | Lossless | 541.00   | 27.01          | 2.804         |
| 547000_5725000.tif | ZSTD     | 2         | 22           | Lossless | 541.00   | 26.94          | 2.813         |
| 547000_5725000.tif | PACKBITS | N/A       | N/A          | Lossless | 1048.03  | 6.018          | 1.302         |
| TOM_RGBI16_471000_5958000.tif | uncompressed | N/A       | N/A          | N/A      | 200.03   | N/A            | 1.144         |
| TOM_RGBI16_471000_5958000.tif | LZW      | 1         | N/A          | Lossless | 247.81   | 2.606          | 0.9336        |
| TOM_RGBI16_471000_5958000.tif | LZW      | 2         | N/A          | Lossless | 219.92   | 3.019          | 1.068         |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 1         | 1            | Lossless | 184.32   | 1.997          | 0.5363        |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 1         | 6 (Default)  | Lossless | 181.81   | 2.537          | 0.5828        |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 1         | 9            | Lossless | 181.38   | 4.937          | 0.5674        |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 2         | 1            | Lossless | 165.28   | 1.963          | 0.5999        |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 2         | 6 (Default)  | Lossless | 166.30   | 2.758          | 0.6691        |
| TOM_RGBI16_471000_5958000.tif | DEFLATE  | 2         | 9            | Lossless | 165.33   | 5.671          | 0.6192        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 1         | 1            | Lossless | 184.43   | 0.978          | 0.3772        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 1         | 9 (Default)  | Lossless | 184.43   | 0.9866         | 0.3827        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 1         | 22           | Lossless | 184.43   | 0.9767         | 0.3895        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 2         | 1            | Lossless | 165.34   | 1.181          | 0.4477        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 2         | 9 (Default)  | Lossless | 165.34   | 1.049          | 0.4509        |
| TOM_RGBI16_471000_5958000.tif | ZSTD     | 2         | 22           | Lossless | 165.34   | 1.049          | 0.4454        |
| TOM_RGBI16_471000_5958000.tif | PACKBITS | N/A       | N/A          | Lossless | 192.26   | 1.126          | 0.1859        |


code created by chatgpt; needs to be tested and check
```python
import os
import glob
import time
import subprocess
from osgeo import gdal

# List of input raster files (update this list or scan a folder)
input_folder = r'D:\Test\test_compression\daten'
input_rasters = glob.glob(input_folder+'/*.tif')  # Add multiple raster files here
output_folder = r'D:\Test\test_compression\results'
output_md = os.path.join(output_folder,"results.md")  # Markdown output file

# Compression methods with predictors, lossless type, and compression levels
compression_methods = {
    # method, predictor, type, zlevel
    "LZW": ([1, 2], "Lossless", [None]),  # No compression level support (N/A)
    "DEFLATE": ([1, 2], "Lossless", [1, 6, 9]),  # Level 1 (fastest), 6 (default), 9 (max compression)
    "ZSTD": ([1, 2], "Lossless", [1, 9, 22]),  # Level 1 (fastest), 9 (default), 22 (max compression)
    "PACKBITS": ([None], "Lossless", [None]),  # No compression level support (N/A)
}

# Default compression levels for reference in the table
default_levels = {
    "DEFLATE": 6,  # GDAL default for DEFLATE
    "ZSTD": 9,  # GDAL default for ZSTD
}

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def get_file_size(file_path):
    """Returns file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def measure_read_time(file_path):
    """Measure the time taken to open and read a raster with GDAL."""
    start_time = time.time()
    dataset = gdal.Open(file_path)
    if dataset:
        dataset.GetRasterBand(1).ReadAsArray()  # Read data into memory
    end_time = time.time()
    return end_time - start_time  # Return reading time

def compress_raster(input_file, output_file, compression, predictor, level):
    """
    Compress raster using gdal_translate and measure time.
    """
    options = f"-co COMPRESS={compression}"
    
    # Add predictor option if applicable
    if predictor:
        options += f" -co PREDICTOR={predictor}"
    
    # Add compression level if applicable
    if level is not None:
        if compression in ["DEFLATE", "ZSTD"]:
            options += f" -co ZLEVEL={level}"
        elif compression == "JPEG":
            options += f" -co QUALITY={level}"

    

    command = f"gdal_translate -of GTiff {options} {input_file} {output_file}"
    print(command)
    start_time = time.time()
    subprocess.run(command)
    end_time = time.time()

    return end_time - start_time  # Return compression time

# Store all results
results = []

# Process each input raster
for input_raster in input_rasters:
    # Get original image size and read time
    uncompressed_size = get_file_size(input_raster)
    uncompressed_read_time = measure_read_time(input_raster)
    results.append((os.path.basename(input_raster), "uncompressed", "N/A", "N/A", "N/A", uncompressed_size, "N/A", uncompressed_read_time))

#     # Process each compression method with predictors and levels
    for compression, (predictors, lossless, levels) in compression_methods.items():
        for predictor in predictors:
            for level in levels:
                # Determine if a compression level is available
                if level is None and compression not in default_levels:
                    level_str = "N/A"
                elif level is None:
                    level_str = "Default"
                elif default_levels.get(compression) == level:
                    level_str = f"{level} (Default)"
                else:
                    level_str = str(level)

                # Construct output filename
                output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}"
                if predictor:
                    output_filename += f"_PRED{predictor}"
                if level is not None:
                    output_filename += f"_LVL{level}"
                output_filename += ".tif"

                output_file = os.path.join(output_folder, output_filename)

                # Measure compression (writing) time
                write_time = compress_raster(input_raster, output_file, compression, predictor, level)

                # Measure decompression (reading) time
                read_time = measure_read_time(output_file)

                # Get file size
                file_size = get_file_size(output_file)

                # Store results
                results.append((os.path.basename(input_raster), compression, predictor if predictor else "N/A", level_str, lossless, file_size, write_time, read_time))

# Write results to Markdown file
with open(output_md, "w") as md_file:
    md_file.write("# Compression Performance Comparison\n\n")
    md_file.write("| Input File | Method   | Predictor | Level         | Type     | Size (MB) | Write Time (s) | Read Time (s) |\n")
    md_file.write("|------------|----------|-----------|--------------|----------|----------|----------------|---------------|\n")
    for file, comp, pred, level, lossless, size, write_t, read_t in results:
        md_file.write(f"| {file:<10} | {comp:<8} | {pred:<9} | {level:<12} | {lossless:<8} | {size:<8.2f} | {write_t:<14.4} | {read_t:<13.4} |\n")

print(f"\nResults saved to {output_md}")
```
