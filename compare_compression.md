# Comparison of raster compression methods 

Input data:
- six Geotiff tiles
- extent: 2000 x 2000 m
- type: 8 bit
- resolution: 0.2 m 


# Output Format: Cloud Optimized Geotiff (COG)
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



```python
import os
import glob
import time
import subprocess
import statistics
from osgeo import gdal

# Directories for input and output files
input_folder = r'D:\Test\test_compression\daten'
output_folder = r'D:\Test\test_compression\results'  # Output directory for results
output_md = os.path.join(output_folder, "results.md")  # Markdown output file

# Scan for input raster files
input_rasters = glob.glob(os.path.join(input_folder, '*.tif'))

# Compression methods with levels and predictors
compression_methods = {
    "WEBP": { "levels": [None], "predictor": None},
    "LZW": { "levels": [None], "predictor": 2},
    "DEFLATE": { "levels": [1, 6, 9], "predictor": 2},
    "ZSTD": { "levels": [1, 9, 22], "predictor": 2},
    "LZMA": { "levels": [1, 6, 9], "predictor": None},
    "PACKBITS": { "levels": [None], "predictor": None},
    "LERC": { "levels": [None], "predictor": None},
    "LERC_DEFLATE": { "levels": [None], "predictor": None},
    "LERC_ZSTD": { "levels": [None], "predictor": None}
    ,"JPEG2000": { "levels": [None], "predictor": None}}

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

def get_file_size(file_path):
    """Returns file size in MB."""
    return os.path.getsize(file_path) / (1024 * 1024)

def measure_read_time(file_path):
    """Measure the time taken to open and read a raster with GDAL."""
    start_time = time.time()
    dataset = gdal.Open(file_path)
    if dataset:
        dataset.GetRasterBand(1).ReadAsArray()  # Read into memory
        dataset = None  # Close dataset
        return round(time.time() - start_time, 2)
    return None

def compress_raster(input_file, output_file, compression=None, predictor=None, level=None):
    """Compress raster using gdal_translate"""
    options = ["-of GTiff"]

    # Add compression type to options
    if compression:
        options.append(f"-co COMPRESS={compression}")

    # Add compression level if provided
    if level:
        options.append(f"-co ZLEVEL={level}")
    
    # Add predictor if necessary
    if predictor:
        options.append(f"-co PREDICTOR={predictor}")

    # Add quality setting for certain lossy methods
    if compression in ["WEBP", "LERC", "LERC_DEFLATE", "LERC_ZSTD", "JPEG2000"]:
        options.append("-co QUALITY=100")

    # Create and run the command
    command = f'gdal_translate {" ".join(options)} "{input_file}" "{output_file}"'
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

# Process each input raster
for input_raster in input_rasters:
    original_file_size = get_file_size(input_raster)
    compare_size = original_file_size
    original_read_time = measure_read_time(input_raster)
    orig_read_time = measure_read_time(input_raster)
    original_file_size_percantage = (original_file_size / compare_size) * 100
    # Store uncompressed GTiff (Original) file stats
    if "GTiff_uncompressed (Original)" not in compression_stats:
        compression_stats["GTiff_uncompressed (Original)"] = {
            'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
    compression_stats["GTiff_uncompressed (Original)"]['sizes'].append(original_file_size)
    compression_stats["GTiff_uncompressed (Original)"]['read_times'].append(original_read_time)
    compression_stats["GTiff_uncompressed (Original)"]['size_percentage'].append(original_file_size_percantage)

           
    # For each compression method, apply and collect results
    for compression, method_data in compression_methods.items():
        levels = method_data['levels']
        predictor = method_data['predictor']
        
        if predictor is None:
            # Normal case for compression methods without predictor=2
            for level in levels:
                tif_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}.tif"
                tif_output_file = os.path.join(output_folder, tif_output_filename)

                print(f"Processing: {compression} with Level {level}")
                tif_write_time = compress_raster(input_raster, tif_output_file, compression, predictor, level)
                if tif_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} due to failure.")
                    continue

                tif_read_time = measure_read_time(tif_output_file)
                tif_file_size = get_file_size(tif_output_file)
                tif_file_size_percantage = (tif_file_size / compare_size) * 100
                print(tif_output_filename+': '+ str(tif_file_size)+', ' +str(tif_file_size_percantage))

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_no_predictor"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    
                
                compression_stats[compression_key]['sizes'].append(tif_file_size)
                compression_stats[compression_key]['size_percentage'].append(tif_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(tif_write_time)
                compression_stats[compression_key]['read_times'].append(tif_read_time)

        # If predictor is 2, run compression twice: once with predictor=2 and once without
        if predictor == 2:
            # Run without predictor (predictor=None)
            for level in levels:
                tif_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_no_predictor.tif"
                tif_output_file = os.path.join(output_folder, tif_output_filename)

                print(f"Processing: {compression} with Level {level} and No Predictor")
                tif_write_time = compress_raster(input_raster, tif_output_file, compression, None, level)
                if tif_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and No Predictor due to failure.")
                    continue

                tif_read_time = measure_read_time(tif_output_file)
                tif_file_size = get_file_size(tif_output_file)
                tif_file_size_percantage = (tif_file_size / compare_size) * 100

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_no_predictor"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                
                compression_stats[compression_key]['sizes'].append(tif_file_size)
                compression_stats[compression_key]['size_percentage'].append(tif_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(tif_write_time)
                compression_stats[compression_key]['read_times'].append(tif_read_time)
            
            # Run with predictor=2
            for level in levels:
                tif_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_predictor2.tif"
                tif_output_file = os.path.join(output_folder, tif_output_filename)

                print(f"Processing: {compression} with Level {level} and Predictor 2")
                tif_write_time = compress_raster(input_raster, tif_output_file, compression, 2, level)
                if tif_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and Predictor 2 due to failure.")
                    continue

                tif_read_time = measure_read_time(tif_output_file)
                tif_file_size = get_file_size(tif_output_file)
                tif_file_size_percantage = (tif_file_size/compare_size) * 100

                # Construct a unique key for each combination of method, level, and predictor
                compression_key = f"{compression}_level{level}_predictor2"

                # Store the statistics for later averaging
                if compression_key not in compression_stats:
                    if level is not None:
                        compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}" + ' ' + f"-co PREDICTOR={predictor}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                    else:
                        compression_stats[compression_key] = {'compression_options': [f"-co PREDICTOR={predictor}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                                
                compression_stats[compression_key]['sizes'].append(tif_file_size)
                compression_stats[compression_key]['size_percentage'].append(tif_file_size_percantage)
                compression_stats[compression_key]['write_times'].append(tif_write_time)
                compression_stats[compression_key]['read_times'].append(tif_read_time)
        

print(compression_stats)

# Calculate averages and standard deviations
summary_stats = {}
# uncompressed_tif_size = compression_stats["tif_uncompressed"]['sizes'][0]  # Uncompressed tif size for percentage calculation

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
