| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Uncompressed COG (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------------------------|---------------------|-------------------------|-----------------------------------------------|-----------------------------|----------------------------|
| GTiff_uncompressed (Original) |                     | 400.01 ± 0.00 | 70.36 ± 2.11  | 0.00 ± 0.00 | 1.74 ± 0.66 |
| COG_uncompressed           |                     | 568.90 ± 16.84 | 100.00 ± 0.00  | 12.44 ± 0.67 | 2.11 ± 0.20 |
| LZW                        |                     | 568.90 ± 16.84 | 100.00 ± 0.00  | 12.54 ± 0.98 | 2.12 ± 0.14 |
| LZW                        | -co PREDICTOR=2     | 393.12 ± 20.21 | 69.08 ± 2.17  | 12.76 ± 0.74 | 2.05 ± 0.13 |
| DEFLATE                    | -co ZLEVEL=1        | 431.79 ± 9.88 | 75.91 ± 0.63  | 13.50 ± 0.85 | 1.20 ± 0.08 |
| DEFLATE                    | -co ZLEVEL=6        | 431.79 ± 9.88 | 75.91 ± 0.63  | 13.33 ± 0.78 | 1.16 ± 0.10 |
| DEFLATE                    | -co ZLEVEL=9        | 431.79 ± 9.88 | 75.91 ± 0.63  | 13.18 ± 0.56 | 1.16 ± 0.05 |
| DEFLATE                    | -co ZLEVEL=1 -co PREDICTOR=2 | 332.98 ± 14.42 | 58.52 ± 1.42  | 15.54 ± 1.06 | 1.34 ± 0.10 |
| DEFLATE                    | -co ZLEVEL=6 -co PREDICTOR=2 | 332.98 ± 14.42 | 58.52 ± 1.42  | 15.34 ± 0.69 | 1.34 ± 0.09 |
| DEFLATE                    | -co ZLEVEL=9 -co PREDICTOR=2 | 332.98 ± 14.42 | 58.52 ± 1.42  | 15.83 ± 1.08 | 1.34 ± 0.10 |
| ZSTD                       | -co ZLEVEL=1        | 437.82 ± 10.11 | 76.97 ± 0.71  | 11.72 ± 0.89 | 0.75 ± 0.10 |
| ZSTD                       | -co ZLEVEL=9        | 437.82 ± 10.11 | 76.97 ± 0.71  | 12.09 ± 0.82 | 0.80 ± 0.18 |
| ZSTD                       | -co ZLEVEL=22       | 437.82 ± 10.11 | 76.97 ± 0.71  | 12.02 ± 0.59 | 0.84 ± 0.22 |
| ZSTD                       | -co ZLEVEL=1 -co PREDICTOR=2 | 333.67 ± 16.47 | 58.64 ± 1.81  | 21.60 ± 0.83 | 1.02 ± 0.09 |
| ZSTD                       | -co ZLEVEL=9 -co PREDICTOR=2 | 333.67 ± 16.47 | 58.64 ± 1.81  | 22.05 ± 1.31 | 1.02 ± 0.08 |
| ZSTD                       | -co ZLEVEL=22 -co PREDICTOR=2 | 333.67 ± 16.47 | 58.64 ± 1.81  | 21.32 ± 0.99 | 1.03 ± 0.13 |
| LZMA                       | -co ZLEVEL=1        | 351.00 ± 11.97 | 61.70 ± 0.90  | 119.58 ± 3.60 | 15.61 ± 0.53 |
| LZMA                       | -co ZLEVEL=6        | 351.00 ± 11.97 | 61.70 ± 0.90  | 117.12 ± 4.26 | 15.28 ± 0.50 |
| LZMA                       | -co ZLEVEL=9        | 351.00 ± 11.97 | 61.70 ± 0.90  | 119.14 ± 5.12 | 15.42 ± 0.81 |
| PACKBITS                   |                     | 512.98 ± 0.01 | 90.24 ± 2.70  | 8.62 ± 1.35 | 0.30 ± 0.06 |
| LERC                       |                     | 365.40 ± 14.19 | 64.23 ± 1.59  | 12.47 ± 0.55 | 2.42 ± 0.24 |
| LERC_DEFLATE               |                     | 362.62 ± 14.48 | 63.74 ± 1.61  | 16.72 ± 1.07 | 2.80 ± 0.36 |
| LERC_ZSTD                  |                     | 363.26 ± 14.29 | 63.85 ± 1.60  | 15.35 ± 0.82 | 2.32 ± 0.10 |



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
    "LERC_ZSTD": { "levels": [None], "predictor": None}}
    # ,"JPEG2000": { "levels": [None], "predictor": None}}

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
    """Compress raster using gdal_translate with COG format."""
    options = ["-of COG"]

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
uncompressed_cog_file = os.path.join(output_folder, "uncompressed_COG.tif")

# Process each input raster
for input_raster in input_rasters:
    original_size = get_file_size(input_raster)
    original_read_time = measure_read_time(input_raster)

    # Process uncompressed COG file first
    cog_uncompressed_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_COG.tif"
    cog_uncompressed_file = os.path.join(output_folder, cog_uncompressed_filename)

    cog_write_time = compress_raster(input_raster, cog_uncompressed_file)
    cog_read_time = measure_read_time(cog_uncompressed_file)
    cog_uncompressed_file_size = get_file_size(cog_uncompressed_file)
    cog_file_size_percantage = (cog_uncompressed_file_size / cog_uncompressed_file_size) * 100
   
    # Original file stats (GTiff)
    orig_read_time = measure_read_time(input_raster)
    original_file_size = get_file_size(input_raster)
    original_file_size_percantage = (original_file_size / cog_uncompressed_file_size) * 100
    # Store uncompressed GTiff (Original) file stats
    if "GTiff_uncompressed (Original)" not in compression_stats:
        compression_stats["GTiff_uncompressed (Original)"] = {
            'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
    compression_stats["GTiff_uncompressed (Original)"]['sizes'].append(original_size)
    compression_stats["GTiff_uncompressed (Original)"]['read_times'].append(original_read_time)
    compression_stats["GTiff_uncompressed (Original)"]['size_percentage'].append(original_file_size_percantage)

    # Store uncompressed COG file stats
    if "COG_uncompressed" not in compression_stats:
        compression_stats["COG_uncompressed"] = {
            'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
    compression_stats["COG_uncompressed"]['sizes'].append(cog_uncompressed_file_size)
    compression_stats["COG_uncompressed"]['size_percentage'].append(cog_file_size_percantage)
    compression_stats["COG_uncompressed"]['write_times'].append(cog_write_time)
    compression_stats["COG_uncompressed"]['read_times'].append(cog_read_time)
            
    # For each compression method, apply and collect results
    for compression, method_data in compression_methods.items():
        levels = method_data['levels']
        predictor = method_data['predictor']
        
        if predictor is None:
            # Normal case for compression methods without predictor=2
            for level in levels:
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_COG.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level}")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, predictor, level)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size / cog_uncompressed_file_size) * 100
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
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_no_predictor_COG.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level} and No Predictor")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, None, level)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and No Predictor due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size / cog_uncompressed_file_size) * 100

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
                cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_predictor2_COG.tif"
                cog_output_file = os.path.join(output_folder, cog_output_filename)

                print(f"Processing: {compression} with Level {level} and Predictor 2")
                cog_write_time = compress_raster(input_raster, cog_output_file, compression, 2, level)
                if cog_write_time is None:
                    print(f"❌ Skipping {compression} with Level {level} and Predictor 2 due to failure.")
                    continue

                cog_read_time = measure_read_time(cog_output_file)
                cog_file_size = get_file_size(cog_output_file)
                cog_file_size_percantage = (cog_file_size/cog_uncompressed_file_size) * 100

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
        
        # else:
        #     # Normal case for compression methods without predictor=2
        #     for level in levels:
        #         cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_level{level}_COG.tif"
        #         cog_output_file = os.path.join(output_folder, cog_output_filename)

        #         print(f"Processing: {compression} with Level {level}")
        #         cog_write_time = compress_raster(input_raster, cog_output_file, compression, predictor, level)
        #         if cog_write_time is None:
                    
        #             (f"❌ Skipping {compression} with Level {level} due to failure.")
        #             continue

        #         cog_read_time = measure_read_time(cog_output_file)
        #         cog_file_size = get_file_size(cog_output_file)
        #         cog_file_size_percantage = (cog_file_size / cog_uncompressed_file_size) * 100
        #         print(cog_file_size_percantage)

        #         # Construct a unique key for each combination of method, level, and predictor
        #         compression_key = f"{compression}_level{level}_no_predictor"

        #         # Store the statistics for later averaging
        #         if level is not None:
        #             compression_stats[compression_key] = {'compression_options': [f"-co ZLEVEL={level}"], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
        #         else:
        #             compression_stats[compression_key] = {'compression_options': [], 'sizes': [], 'size_percentage': [], 'write_times': [], 'read_times': []}
                
        #         compression_stats[compression_key]['sizes'].append(cog_file_size)
        #         compression_stats[compression_key]['size_percentage'].append(cog_file_size_percantage)
        #         compression_stats[compression_key]['write_times'].append(cog_write_time)
        #         compression_stats[compression_key]['read_times'].append(cog_read_time)

print(compression_stats)

# Calculate averages and standard deviations
summary_stats = {}
# uncompressed_cog_size = compression_stats["COG_uncompressed"]['sizes'][0]  # Uncompressed COG size for percentage calculation

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
    md_file.write("| Method                     | Compression Options | Mean Size (MB) ± StdDev | Size Compared to Uncompressed COG (%) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |\n")
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

```
