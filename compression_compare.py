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
input_rasters = glob.glob(os.path.join(input_folder, '*.tif'))

# Output format
output_format = 'GTiff '  # Output format for gdal_translate, shoose between 'GTiff' or 'COG'
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
        cog_file_size_percantage = (cog_uncompressed_file_size / compare_size) * 100

    original_file_size = get_file_size(input_raster)
    if output_format == 'GTiff':
        compare_size = original_file_size
        compare_field = 'Size Compared to Original'
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
                cog_file_size_percantage = (cog_file_size / compare_size) * 100
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
                cog_file_size_percantage = (cog_file_size / compare_size) * 100

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
                cog_file_size_percantage = (cog_file_size/compare_size) * 100

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
