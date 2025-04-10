#Test 1 Output Format: GTiff

| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Original (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 400.01 ± 0.00 | 100.00 ± 0.00  | 0.00 ± 0.00 | 2.35 ± 1.40 |
| LZW                        |                     | 435.80 ± 11.11 | 108.95 ± 2.78  | 5.16 ± 0.36 | 1.99 ± 0.05 |
| LZW                        | -co PREDICTOR=2     | 286.12 ± 14.42 | 71.53 ± 3.61  | 5.23 ± 0.10 | 1.95 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=1        | 340.94 ± 3.45 | 85.23 ± 0.86  | 3.48 ± 0.20 | 1.06 ± 0.04 |
| DEFLATE                    | -co ZLEVEL=6        | 333.64 ± 4.90 | 83.41 ± 1.23  | 5.28 ± 0.17 | 1.19 ± 0.04 |
| DEFLATE                    | -co ZLEVEL=9        | 332.28 ± 5.62 | 83.07 ± 1.41  | 11.25 ± 0.54 | 1.19 ± 0.06 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 253.05 ± 10.20 | 63.26 ± 2.55  | 3.68 ± 0.08 | 1.32 ± 0.04 |
| DEFLATE                    | -co ZLEVEL=6 -co PREDICTOR=2 | 250.67 ± 9.29 | 62.67 ± 2.32  | 6.54 ± 0.24 | 1.44 ± 0.08 |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 244.01 ± 9.99 | 61.00 ± 2.50  | 18.45 ± 1.14 | 1.46 ± 0.07 |
| ZSTD                       | -co ZLEVEL=1        | 344.78 ± 2.46 | 86.19 ± 0.62  | 1.82 ± 0.16 | 0.73 ± 0.04 |
| ZSTD                       | -co ZLEVEL=9        | 344.78 ± 2.46 | 86.19 ± 0.62  | 1.87 ± 0.17 | 0.74 ± 0.05 |
| ZSTD                       | -co ZLEVEL=22       | 344.78 ± 2.46 | 86.19 ± 0.62  | 1.86 ± 0.14 | 0.72 ± 0.04 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 263.40 ± 11.71 | 65.85 ± 2.93  | 8.02 ± 0.30 | 0.85 ± 0.03 |
| ZSTD                       | -co ZLEVEL=9 -co PREDICTOR=2 | 263.40 ± 11.71 | 65.85 ± 2.93  | 8.01 ± 0.29 | 0.86 ± 0.03 |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 263.40 ± 11.71 | 65.85 ± 2.93  | 8.03 ± 0.35 | 0.85 ± 0.03 |
| LZMA                       | -co ZLEVEL=1        | 271.26 ± 7.11 | 67.81 ± 1.78  | 70.28 ± 2.52 | 16.12 ± 0.37 |
| LZMA                       | -co ZLEVEL=6        | 271.26 ± 7.11 | 67.81 ± 1.78  | 70.86 ± 3.61 | 15.98 ± 0.34 |
| LZMA                       | -co ZLEVEL=9        | 271.26 ± 7.11 | 67.81 ± 1.78  | 70.64 ± 3.04 | 15.92 ± 0.36 |
| PACKBITS                   |                     | 384.48 ± 0.03 | 96.12 ± 0.01  | 2.02 ± 0.08 | 0.33 ± 0.05 |
| LERC                       |                     | 271.04 ± 10.07 | 67.76 ± 2.52  | 7.41 ± 0.09 | 2.47 ± 0.07 |
| LERC_DEFLATE               |                     | 271.13 ± 10.10 | 67.78 ± 2.52  | 9.81 ± 0.18 | 2.66 ± 0.05 |
| LERC_ZSTD                  |                     | 271.14 ± 10.07 | 67.78 ± 2.52  | 7.89 ± 0.12 | 2.50 ± 0.06 |
| JPEG2000                   |                     | 381.53 ± 0.00 | 95.38 ± 0.00  | 0.79 ± 0.22 | 0.33 ± 0.04 |


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
    md_file.write("| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Original (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |\n")
    md_file.write("|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|\n")
    
    # Iterate through the summary statistics and write each method's results
    for comp, stats in summary_stats.items():
   
        # Extract the statistics for each compression method
        if comp in ['GTiff_uncompressed (Original)', 'tif_uncompressed']:
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

```
