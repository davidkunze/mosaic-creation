import os
import time
import subprocess
from osgeo import gdal

# Input raster file
input_raster = "input.tif"  # Change to your raster file
output_folder = "compressed_outputs"
output_md = "results.md"  # Markdown output file

# Compression methods with predictors, lossless type, and compression levels
compression_methods = {
    "LZW": ([1, 2, 3], "Lossless", [None]),  # No compression level support (N/A)
    "DEFLATE": ([1, 2, 3], "Lossless", [1, 6, 9]),  # Level 1 (fastest), 6 (default), 9 (max compression)
    "ZSTD": ([1, 2, 3], "Lossless", [1, 9, 22]),  # Level 1 (fastest), 9 (default), 22 (max compression)
    "JPEG": ([None], "Lossy", [100, 10]),  # Quality 100 (best), 10 (worst)
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

    # Special case for JPEG (requires photometric setting)
    if compression == "JPEG":
        options += " -co PHOTOMETRIC=YCBCR"

    command = f"gdal_translate -of GTiff {options} {input_file} {output_file}"
    
    start_time = time.time()
    subprocess.run(command, shell=True, check=True)
    end_time = time.time()

    return end_time - start_time  # Return compression time

# Get original image size and read time
original_size = get_file_size(input_raster)
original_read_time = measure_read_time(input_raster)

# Store results
results = [("Original", "N/A", "N/A", "N/A", original_size, "N/A", original_read_time)]

# Process each compression method with predictors and levels
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
            output_filename = f"compressed_{compression}"
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
            results.append((compression, predictor if predictor else "N/A", level_str, lossless, file_size, write_time, read_time))

# Write results to Markdown file
with open(output_md, "w") as md_file:
    md_file.write("# Compression Performance Comparison\n\n")
    md_file.write("| Method   | Predictor | Level         | Type     | Size (MB) | Write Time (s) | Read Time (s) |\n")
    md_file.write("|----------|-----------|--------------|----------|----------|----------------|---------------|\n")
    for comp, pred, level, lossless, size, write_t, read_t in results:
        md_file.write(f"| {comp:<8} | {pred:<9} | {level:<12} | {lossless:<8} | {size:<8.2f} | {write_t:<14.4f} | {read_t:<13.4f} |\n")

print(f"\nResults saved to {output_md}")
