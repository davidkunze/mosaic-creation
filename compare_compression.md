# Comparison of lossless raster compression methods 

Input data:
- format: uncompressed GTiffs
- number of input tiles: 6
- data type: same rasters tested with 8 bit unsigned integer and 16 bit unsigned integer
- tile size: 2000 x 2000 m
- spatial resolution: 0.2 m

# Output Format: GTiff - 8 Bit unsigned integer

| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Original (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 400.01 ± 0.00 | 100.00 ± 0.00  | 0.00 ± 0.00 | 1.95 ± 0.11 |
| LZW                        |                     | 435.80 ± 11.11 | 108.95 ± 2.78  | 5.35 ± 0.61 | 2.02 ± 0.22 |
| LZW                        | -co PREDICTOR=2     | 286.12 ± 14.42 | 71.53 ± 3.61  | 5.48 ± 0.38 | 1.96 ± 0.11 |
| DEFLATE                    | -co ZLEVEL=1        | 340.94 ± 3.45 | 85.23 ± 0.86  | 3.74 ± 0.28 | 1.21 ± 0.27 |
| DEFLATE                    | -co ZLEVEL=6        | 333.64 ± 4.90 | 83.41 ± 1.23  | 5.53 ± 0.42 | 1.20 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=9        | 332.28 ± 5.62 | 83.07 ± 1.41  | 11.31 ± 1.02 | 1.17 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 253.05 ± 10.20 | 63.26 ± 2.55  | 3.84 ± 0.12 | 1.28 ± 0.06 |
| ***DEFLATE***                    | ***-co ZLEVEL=6 -co PREDICTOR=2*** | ***250.67 ± 9.29*** | ***62.67 ± 2.32***  | ***6.97 ± 0.63*** | ***1.39 ± 0.06*** |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 244.01 ± 9.99 | 61.00 ± 2.50 | 20.30 ± 2.86 | 1.47 ± 0.07 |
| ZSTD                       | -co ZLEVEL=1        | 344.99 ± 2.65 | 86.25 ± 0.66  | 1.30 ± 0.07 | 0.77 ± 0.04 |
| ZSTD                       | -co ZLEVEL=9        | 344.78 ± 2.46 | 86.19 ± 0.62  | 2.06 ± 0.45 | 0.79 ± 0.04 |
| ZSTD                       | -co ZLEVEL=22       | 334.87 ± 5.60 | 83.72 ± 1.40  | 139.51 ± 12.38 | 0.98 ± 0.05 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 269.17 ± 10.12 | 67.29 ± 2.53  | 1.43 ± 0.07 | 0.73 ± 0.04 |
| ***ZSTD***                       | ***-co ZLEVEL=9 -co PREDICTOR=2*** | ***263.40 ± 11.71*** | ***65.85 ± 2.93***  | ***8.26 ± 0.53*** | ***0.88 ± 0.02*** |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 242.91 ± 10.35 | **60.73 ± 2.59**  | 145.91 ± 12.11 | 1.50 ± 0.05 |
| LZMA                       | -co ZLEVEL=1        | 271.26 ± 7.11 | 67.81 ± 1.78  | 78.91 ± 6.65 | 16.01 ± 0.76 |
| LZMA                       | -co ZLEVEL=6        | 271.26 ± 7.11 | 67.81 ± 1.78  | 79.14 ± 4.64 | 15.92 ± 0.71 |
| LZMA                       | -co ZLEVEL=9        | 271.26 ± 7.11 | 67.81 ± 1.78  | 77.58 ± 6.60 | 15.94 ± 1.05 |
| PACKBITS                   |                     | 384.48 ± 0.03 | 96.12 ± 0.01  | **2.07 ± 0.17** | **0.35 ± 0.04** |
| LERC                       |                     | 271.04 ± 10.07 | 67.76 ± 2.52  | 7.89 ± 0.58 | 2.65 ± 0.18 |
| LERC_DEFLATE               |                     | 271.13 ± 10.10 | 67.78 ± 2.52  | 10.57 ± 1.03 | 2.86 ± 0.31 |
| LERC_ZSTD                  |                     | 271.14 ± 10.07 | 67.78 ± 2.52  | 8.60 ± 0.82 | 2.76 ± 0.33 |

# Output Format: GTiff - 16 Bit unsigned integer

| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Original (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 800.00 ± 0.00 | 100.00 ± 0.00  | 0.00 ± 0.00 | 4.09 ± 1.60 |
| LZW                        |                     | 1024.87 ± 2.65 | 128.11 ± 0.33  | 9.20 ± 0.19 | 6.62 ± 0.20 |
| LZW                        | -co PREDICTOR=2     | 971.56 ± 11.73 | 121.44 ± 1.47  | 11.36 ± 0.23 | 7.11 ± 0.27 |
| DEFLATE                    | -co ZLEVEL=1        | 748.31 ± 1.45 | 93.54 ± 0.18  | 7.78 ± 0.11 | 5.38 ± 0.15 |
| DEFLATE                    | -co ZLEVEL=6        | 745.87 ± 1.88 | 93.23 ± 0.23  | 10.07 ± 0.11 | 5.39 ± 0.09 |
| DEFLATE                    | -co ZLEVEL=9        | 745.09 ± 1.93 | 93.14 ± 0.24  | 20.14 ± 0.22 | 5.33 ± 0.10 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 703.12 ± 6.62 | 87.89 ± 0.83  | 7.85 ± 0.13 | 5.58 ± 0.14 |
| DEFLATE                    | -co ZLEVEL=6 -co PREDICTOR=2 | 703.46 ± 6.39 | 87.93 ± 0.80  | 10.34 ± 0.09 | 5.61 ± 0.07 |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 702.73 ± 6.52 | 87.84 ± 0.82  | 21.33 ± 0.32 | 5.49 ± 0.11 |
| ZSTD                       | -co ZLEVEL=1        | 754.15 ± 4.23 | 94.27 ± 0.53  | 2.30 ± 0.25 | 4.61 ± 0.29 |
| ZSTD                       | -co ZLEVEL=9        | 754.15 ± 4.22 | 94.27 ± 0.53  | 2.96 ± 0.35 | 4.50 ± 0.28 |
| ZSTD                       | -co ZLEVEL=22       | 752.93 ± 4.13 | 94.12 ± 0.52  | 206.25 ± 3.62 | 4.49 ± 0.19 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 702.95 ± 6.60 | 87.87 ± 0.83  | 2.70 ± 0.10 | 4.99 ± 0.09 |
| ZSTD                       | -co ZLEVEL=9 -co PREDICTOR=2 | 702.95 ± 6.60 | 87.87 ± 0.83  | 3.39 ± 0.21 | 5.11 ± 0.18 |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 702.46 ± 7.20 | 87.81 ± 0.90  | 221.44 ± 14.93 | 5.22 ± 0.07 |
| LZMA                       | -co ZLEVEL=1        | 750.38 ± 4.21 | 93.80 ± 0.53  | 133.26 ± 2.66 | 41.60 ± 0.20 |
| LZMA                       | -co ZLEVEL=6        | 750.38 ± 4.21 | 93.80 ± 0.53  | 135.80 ± 4.50 | 41.60 ± 0.35 |
| LZMA                       | -co ZLEVEL=9        | 750.38 ± 4.21 | 93.80 ± 0.53  | 135.06 ± 5.41 | 41.69 ± 0.17 |
| PACKBITS                   |                     | 768.97 ± 0.00 | 96.12 ± 0.00  | 3.87 ± 0.05 | 3.95 ± 0.07 |
| LERC                       |                     | 763.85 ± 0.00 | 95.48 ± 0.00  | 5.06 ± 0.17 | 4.79 ± 0.54 |
| LERC_DEFLATE               |                     | 746.58 ± 1.88 | 93.32 ± 0.23  | 13.66 ± 0.14 | 5.90 ± 0.10 |
| LERC_ZSTD                  |                     | 754.90 ± 4.24 | 94.36 ± 0.53  | 6.30 ± 0.11 | 4.95 ± 0.27 |

# Output Format: COG (CLoud Optimized Geotiff) - 8 Bit unsigned integer

| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to uncompressed COG (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 400.01 ± 0.00 | 70.36 ± 2.11  | 0.00 ± 0.00 | 0.26 ± 0.06 |
| COG_uncompressed           |                     | 568.90 ± 16.84 | 100.00 ± 0.00  | 15.44 ± 3.22 | 2.00 ± 0.19 |
| LZW                        |                     | 568.90 ± 16.84 | 100.00 ± 0.00  | 12.21 ± 0.55 | 1.95 ± 0.11 |
| LZW                        | -co PREDICTOR=2     | 393.12 ± 20.21 | 69.08 ± 2.17  | 12.43 ± 0.19 | 1.82 ± 0.09 |
| DEFLATE                    | -co ZLEVEL=1        | 434.68 ± 8.99 | 76.42 ± 0.80  | 10.48 ± 0.42 | 1.00 ± 0.05 |
| DEFLATE                    | -co ZLEVEL=6        | 431.79 ± 9.88 | 75.91 ± 0.63  | 12.82 ± 0.28 | 1.10 ± 0.07 |
| DEFLATE                    | -co ZLEVEL=9        | 426.70 ± 10.49 | 75.01 ± 0.52  | 24.30 ± 1.68 | 1.18 ± 0.07 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 334.91 ± 14.30 | 58.86 ± 1.50  | 10.46 ± 0.19 | 1.20 ± 0.07 |
| DEFLATE                    | -co ZLEVEL=6 -co PREDICTOR=2 | 332.98 ± 14.42 | 58.52 ± 1.42  | 15.12 ± 0.64 | 1.28 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 322.60 ± 14.10 | 56.69 ± 1.35  | 34.81 ± 2.82 | 1.19 ± 0.09 |
| ZSTD                       | -co ZLEVEL=1        | 440.55 ± 6.93 | 77.47 ± 1.20  | 6.89 ± 0.13 | 0.72 ± 0.06 |
| ZSTD                       | -co ZLEVEL=9        | 437.81 ± 10.12 | 76.97 ± 0.71  | 11.55 ± 0.96 | 0.71 ± 0.06 |
| ZSTD                       | -co ZLEVEL=22       | 421.60 ± 11.53 | 74.11 ± 0.48  | 267.60 ± 4.10 | 1.21 ± 0.08 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 363.39 ± 14.84 | 63.87 ± 1.60  | 7.50 ± 0.38 | 0.68 ± 0.07 |
| ZSTD                       | -co ZLEVEL=9 -co PREDICTOR=2 | 333.67 ± 16.47 | 58.64 ± 1.81  | 21.38 ± 1.88 | 1.05 ± 0.12 |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 305.77 ± 13.20 | 53.74 ± 1.24  | 307.34 ± 16.07 | 1.43 ± 0.08 |
| LZMA                       | -co ZLEVEL=1        | 370.69 ± 10.89 | 65.17 ± 1.01  | 70.72 ± 2.31 | 13.82 ± 0.48 |
| LZMA                       | -co ZLEVEL=6        | 351.00 ± 11.97 | 61.70 ± 0.90  | 120.44 ± 7.65 | 14.30 ± 0.49 |
| LZMA                       | -co ZLEVEL=9        | 351.00 ± 11.97 | 61.70 ± 0.90  | 135.70 ± 10.00 | 14.35 ± 0.47 |
| PACKBITS                   |                     | 512.98 ± 0.01 | 90.24 ± 2.70  | 7.88 ± 0.48 | 0.29 ± 0.07 |
| LERC                       |                     | 365.40 ± 14.19 | 64.23 ± 1.59  | 12.43 ± 0.73 | 2.37 ± 0.12 |
| LERC_DEFLATE               |                     | 362.62 ± 14.48 | 63.74 ± 1.61  | 16.21 ± 0.48 | 2.70 ± 0.14 |
| LERC_ZSTD                  |                     | 363.26 ± 14.29 | 63.85 ± 1.60  | 15.31 ± 0.89 | 2.37 ± 0.13 |

# Output Format: COG (CLoud Optimized Geotiff) - 16 Bit unsigned integer

| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to uncompressed COG (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 800.00 ± 0.00 | 58.52 ± 0.15  | 0.00 ± 0.00 | 0.55 ± 0.09 |
| COG_uncompressed           |                     | 1367.07 ± 3.49 | 100.00 ± 0.00  | 27.69 ± 4.29 | 3.53 ± 0.18 |
| LZW                        |                     | 1367.07 ± 3.49 | 100.00 ± 0.00  | 20.48 ± 0.28 | 3.56 ± 0.20 |
| LZW                        | -co PREDICTOR=2     | 1301.14 ± 16.32 | 95.18 ± 1.04  | 23.73 ± 0.41 | 3.91 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=1        | 989.38 ± 2.85 | 72.37 ± 0.04  | 17.99 ± 0.23 | 2.12 ± 0.09 |
| DEFLATE                    | -co ZLEVEL=6        | 989.91 ± 2.96 | 72.41 ± 0.04  | 20.94 ± 0.25 | 2.13 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=9        | 989.27 ± 3.29 | 72.36 ± 0.06  | 37.96 ± 0.44 | 2.14 ± 0.12 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 939.20 ± 9.64 | 68.70 ± 0.60  | 18.73 ± 0.25 | 2.47 ± 0.19 |
| DEFLATE                    | -co ZLEVEL=6 -co PREDICTOR=2 | 939.75 ± 9.23 | 68.74 ± 0.57  | 22.30 ± 0.37 | 2.52 ± 0.13 |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 937.48 ± 9.84 | 68.58 ± 0.61  | 41.17 ± 0.54 | 2.55 ± 0.06 |
| ZSTD                       | -co ZLEVEL=1        | 990.34 ± 3.31 | 72.44 ± 0.06  | 10.77 ± 0.22 | 1.65 ± 0.12 |
| ZSTD                       | -co ZLEVEL=9        | 990.25 ± 3.35 | 72.44 ± 0.07  | 14.62 ± 0.28 | 1.61 ± 0.12 |
| ZSTD                       | -co ZLEVEL=22       | 989.66 ± 4.34 | 72.39 ± 0.13  | 320.72 ± 1.42 | 1.73 ± 0.22 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 938.89 ± 9.61 | 68.68 ± 0.60  | 12.44 ± 1.53 | 1.93 ± 0.14 |
| ZSTD                       | -co ZLEVEL=9 -co PREDICTOR=2 | 938.73 ± 9.70 | 68.67 ± 0.61  | 15.52 ± 0.34 | 1.88 ± 0.11 |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 937.29 ± 10.72 | 68.56 ± 0.67  | 345.85 ± 3.07 | 3.59 ± 3.10 |
| LZMA                       | -co ZLEVEL=1        | 975.64 ± 9.97 | 71.37 ± 0.59  | 191.21 ± 6.82 | 35.33 ± 0.68 |
| LZMA                       | -co ZLEVEL=6        | 966.47 ± 11.56 | 70.70 ± 0.71  | 225.86 ± 10.95 | 35.24 ± 0.67 |
| LZMA                       | -co ZLEVEL=9        | 966.47 ± 11.56 | 70.70 ± 0.71  | 237.45 ± 8.52 | 35.12 ± 0.41 |
| PACKBITS                   |                     | 1025.93 ± 0.00 | 75.05 ± 0.19  | 15.56 ± 4.75 | 0.84 ± 0.17 |
| LERC                       |                     | 955.36 ± 16.13 | 69.88 ± 1.06  | 15.29 ± 0.39 | 2.41 ± 0.12 |
| LERC_DEFLATE               |                     | 951.24 ± 16.29 | 69.58 ± 1.07  | 26.32 ± 0.39 | 3.75 ± 0.15 |
| LERC_ZSTD                  |                     | 955.01 ± 16.12 | 69.86 ± 1.06  | 19.31 ± 0.23 | 2.45 ± 0.08 |


```python
import os
import glob
import time
import subprocess
import statistics
from osgeo import gdal

# Directories for input and output files
input_folder = r'D:\Test\test_compression_2\daten\8bit'
output_folder = r'D:\Test\test_compression_2\results\8bit'  # Output directory for results


# Scan for input raster files
input_rasters = glob.glob(os.path.join(input_folder, '***.tif'))

# Output format
output_format = 'GTiff'  # Output format for gdal_translate, shoose between 'GTiff' or 'COG'
output_md = os.path.join(output_folder, f"results_{output_format}.md")  # Markdown output file

# Compression methods with levels and predictors
compression_methods = {
    "WEBP": { "levels": [None], "predictor": None, "quality": 100},
    "LZW": { "levels": [None], "predictor": 2, "quality": None},
    "DEFLATE": { "levels": [1, 6, 9], "predictor": 2, "quality": None},
    "ZSTD": { "levels": [1, 9, 22], "predictor": 2, "quality": None},
    "LZMA": { "levels": [1, 6, 9], "predictor": None, "quality": None},
    "PACKBITS": { "levels": [None], "predictor": None, "quality": None},
    "LERC": { "levels": [None], "predictor": None, "quality": 100},
    "LERC_DEFLATE": { "levels": [None], "predictor": None, "quality": 100},
    "LERC_ZSTD": { "levels": [None], "predictor": None, "quality": 100}}

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

def get_file_size(file_path):
    """Returns file size in MB."""
    return os.path.getsize(file_path) / (1024 *** 1024)

def measure_read_time(file_path):
    """Measure the time taken to open and read a raster with GDAL."""
    start_time = time.time()
    dataset = gdal.Open(file_path)
    if dataset:
        dataset.GetRasterBand(1).ReadAsArray()  # Read into memory
        dataset = None  # Close dataset
        return round(time.time() - start_time, 2)
    return None

def compress_raster(input_file, output_file, compression=None, predictor=None, level=None, quality=None):
    """Compress raster using gdal_translate"""
    options = [f"-of {output_format}"]

    # Add compression type to options
    if compression:
        options.append(f"-co COMPRESS={compression}")

    # Add compression level if provided
    if level:
        if output_format == 'GTiff':
            if compression == 'ZSTD':
                options.append(f"-co ZSTD_LEVEL={level}")
            else:
                options.append(f"-co ZLEVEL={level}")
        if output_format == 'COG':
            options.append(f"-co LEVEL={level}")
    # Add predictor if necessary
    if predictor:
        options.append(f"-co PREDICTOR={predictor}") 
    # Add quality if necessary       
    if quality:
        if compression == 'WEBP':
            if output_format == 'GTiff':
                options.append(f"-co WEBP_LOSSLESS=Yes")
            if output_format == 'COG':
                options.append(f"-co QUALITY={quality}")   
        if compression in ['LERC', 'LERC_DEFLATE', 'LERC_ZSTD']:
            options.append(f"-co MAX_Z_ERROR=0")

 

    # Create and run the command
    osgeo4w_shell = r"C:\Program Files\QGIS 3.36.0\OSGeo4W.bat"
    command = f'gdal_translate {" ".join(options)} {input_file} {output_file}'
    print(f"Executing: {command}")
    start_time = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
        return round(time.time() - start_time, 2)
    except subprocess.CalledProcessError:
        print(f"❌ Error compressing {input_file} with {compression if compression else 'NO COMPRESSION'}")
        return None

# Store results for markdown output
compression_stats = {}
uncompressed_cog_file = os.path.join(output_folder, "uncompressed_COG.tif")

# Process each input raster
for input_raster in input_rasters:
      # Process uncompressed COG file first
    if output_format == 'COG':
        cog_uncompressed_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{output_format}.tif"
        cog_uncompressed_file = os.path.join(output_folder, cog_uncompressed_filename)
        cog_write_time = compress_raster(input_raster, cog_uncompressed_file)
        cog_read_time = measure_read_time(cog_uncompressed_file)
        cog_uncompressed_file_size = get_file_size(cog_uncompressed_file)
        compare_size = cog_uncompressed_file_size
        compare_field = 'Size Compared to uncompressed COG'
        cog_file_size_percantage = (cog_uncompressed_file_size / compare_size) *** 100

    original_file_size = get_file_size(input_raster)
    if output_format == 'GTiff':
        compare_size = original_file_size
        compare_field = 'Size Compared to Original'
    original_read_time = measure_read_time(input_raster)
    orig_read_time = measure_read_time(input_raster)
    original_file_size_percantage = (original_file_size / compare_size) *** 100

    # Store uncompressed GTiff (Original) file stats
    if "GTiff_uncompressed (Original)" not in compression_stats:
        compression_stats["GTiff_uncompressed (Original)"] = {
            'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
    compression_stats["GTiff_uncompressed (Original)"]['sizes'].append(original_file_size)
    compression_stats["GTiff_uncompressed (Original)"]['read_times'].append(original_read_time)
    compression_stats["GTiff_uncompressed (Original)"]['size_percentage'].append(original_file_size_percantage)
    
    # Store uncompressed COG file stats
    if output_format == 'COG':
        if "COG_uncompressed" not in compression_stats:
            compression_stats["COG_uncompressed"] = {
                'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
        compression_stats["COG_uncompressed"]['sizes'].append(compare_size)
        compression_stats["COG_uncompressed"]['size_percentage'].append(cog_file_size_percantage)
        compression_stats["COG_uncompressed"]['write_times'].append(cog_write_time)
        compression_stats["COG_uncompressed"]['read_times'].append(cog_read_time)
            
    # For each compression method, apply and collect results
    for compression, method_data in compression_methods.items():
        levels = method_data['levels']
        predictor = method_data['predictor']
        quality = method_data['quality']

        if predictor is None:
            # Normal case for compression methods without predictor=2
            for level in levels:
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_{output_format}.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level}")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, predictor, level, quality)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size / compare_size) *** 100
                print(cog_output_filename+': '+ str(cog_file_size)+', ' +str(cog_file_size_percantage))

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_no_predictor"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    
                
                compression_stats[compression_key]['sizes'].append(cog_file_size)
                compression_stats[compression_key]['size_percentage'].append(cog_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(cog_write_time)
                compression_stats[compression_key]['read_times'].append(cog_read_time)

        # If predictor is 2, run compression twice: once with predictor=2 and once without
        if predictor == 2:
            # Run without predictor (predictor=None)
            for level in levels:
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_no_predictor_{output_format}.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level} and No Predictor")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, None, level, quality)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and No Predictor due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size / compare_size) *** 100

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_no_predictor"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                
                compression_stats[compression_key]['sizes'].append(cog_file_size)
                compression_stats[compression_key]['size_percentage'].append(cog_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(cog_write_time)
                compression_stats[compression_key]['read_times'].append(cog_read_time)
            
            # Run with predictor=2
            for level in levels:
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_predictor2_{output_format}.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level} and Predictor 2")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, 2, level, quality)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and Predictor 2 due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size/compare_size) *** 100

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_predictor2"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}" + ' ' + f"-co PREDICTOR={predictor}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [f"-co PREDICTOR={predictor}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                                
                compression_stats[compression_key]['sizes'].append(cog_file_size)
                compression_stats[compression_key]['size_percentage'].append(cog_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(cog_write_time)
                compression_stats[compression_key]['read_times'].append(cog_read_time)
        

print(compression_stats)

# Calculate averages and standard deviations
summary_stats = {}

for comp, stats in compression_stats.items():
    compression_options = '' if stats['compression_options'] == [] else stats['compression_options'][0]
    avg_size = statistics.mean(stats['sizes'])
    std_size = statistics.stdev(stats['sizes']) if len(stats['sizes']) > 1 else 0
    size_percentage = statistics.mean(stats['size_percentage']) if len(stats['size_percentage']) > 1 else 0
    std_percentage = statistics.stdev(stats['size_percentage']) if len(stats['size_percentage']) > 1 else 0
    avg_write_time = statistics.mean(stats['write_times']) if stats['write_times'] else 0
    std_write_time = statistics.stdev(stats['write_times']) if len(stats['write_times']) > 1 else 0
    avg_read_time = statistics.mean(stats['read_times'])
    std_read_time = statistics.stdev(stats['read_times']) if len(stats['read_times']) > 1 else 0
    

    summary_stats[comp] = {
        'compression_options': compression_options,
        'avg_size': avg_size,
        'std_size': std_size,
        'avg_write_time': avg_write_time,
        'std_write_time': std_write_time,
        'avg_read_time': avg_read_time,
        'std_read_time': std_read_time,
        'size_percentage': size_percentage,
        'std_percentage': std_percentage
    }


# Writing results to markdown file
with open(output_md, 'w') as md_file:
    # Write the header for the Markdown table
    md_file.write("| Method                     | Compression Options | Mean Size (MB) ± StdDev | "+compare_field+" (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |\n")
    md_file.write("|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|\n")
    
    # Iterate through the summary statistics and write each method's results
    for comp, stats in summary_stats.items():
   
        # Extract the statistics for each compression method
        if comp in ['GTiff_uncompressed (Original)', 'COG_uncompressed']:
            comp=comp
        elif comp in ['LERC_DEFLATE_levelNone_no_predictor','LERC_ZSTD_levelNone_no_predictor']:
            comp = '_'.join(comp.split('_')[:2])
        else:
            comp = comp.split('_')[0]   
        compression_options = stats['compression_options']
        mean_size = stats['avg_size']
        std_size = stats['std_size']
        size_percentage = stats['size_percentage']
        std_percentage = stats['std_percentage']
        mean_write_time = stats['avg_write_time']
        std_write_time = stats['std_write_time']
        mean_read_time = stats['avg_read_time']
        std_read_time = stats['std_read_time']
        
              
        # Write the statistics to the markdown table
        md_file.write(f"| {comp:<26} | {compression_options:<19} | {mean_size:.2f} ± {std_size:.2f} | {size_percentage:.2f} ± {std_percentage:.2f}  | {mean_write_time:.2f} ± {std_write_time:.2f} | {mean_read_time:.2f} ± {std_read_time:.2f} |\n")
    }


# Writing results to markdown file
with open(output_md, 'w') as md_file:
    # Write the header for the Markdown table
    md_file.write("| Method                     | Compression Options                | Mean Size (MB) ± StdDev | Size Compared to Original (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |\n")
    md_file.write("|----------------------------|------------------------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|\n")
    
    # Iterate through the summary statistics and write each method's results
    for comp, stats in summary_stats.items():
   
        # Extract the statistics for each compression method
        if comp in ['GTiff_uncompressed (Original)', 'tif_uncompressed']:
            comp=comp
        elif comp.startswith(('LERC_DEFLATE','LERC_ZSTD')):
            comp = '_'.join(comp.split('_')[:2])
        else:
            comp = comp.split('_')[0]   
        compression_options = stats['compression_options']
        mean_size = stats['avg_size']
        std_size = stats['std_size']
        size_percentage = stats['size_percentage']
        std_percentage = stats['std_percentage']
        mean_write_time = stats['avg_write_time']
        std_write_time = stats['std_write_time']
        mean_read_time = stats['avg_read_time']
        std_read_time = stats['std_read_time']
        
              
        # Write the statistics to the markdown table
        md_file.write(f"| {comp:<26} | {compression_options:<19} | {mean_size:.2f} ± {std_size:.2f} | {size_percentage:.2f} ± {std_percentage:.2f}  | {mean_write_time:.2f} ± {std_write_time:.2f} | {mean_read_time:.2f} ± {std_read_time:.2f} |\n")
```
