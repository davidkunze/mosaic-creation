

| Method   | Compression Options | Mean Size (MB) ± StdDev | Mean Write Time (s) ± StdDev | Mean Read Time (s) ± StdDev |
|----------|----------------------|------------------------|------------------------|------------------------|
| Original GTIFF (Uncompressed) |  | 400.01 ± 0.0 | - ± - | 0.69 ± 0.67 |
| COG (Uncompressed) |  | 568.9 ± 16.84 | 13.2 ± 1.31 | 2.08 ± 0.08 |
| DEFLATE | Predictor=NO, Level=1 | 434.68 ± 8.99 | 13.33 ± 0.84 | 1.11 ± 0.09 |
| DEFLATE | Predictor=NO, Level=6 | 431.79 ± 9.88 | 16.31 ± 0.57 | 1.22 ± 0.13 |
| DEFLATE | Predictor=NO, Level=9 | 426.7 ± 10.49 | 26.45 ± 1.63 | 1.15 ± 0.05 |
| DEFLATE | Predictor=YES, Level=1 | 334.91 ± 14.3 | 12.11 ± 0.72 | 1.19 ± 0.03 |
| DEFLATE | Predictor=YES, Level=6 | 332.98 ± 14.42 | 16.65 ± 0.86 | 1.27 ± 0.12 |
| DEFLATE | Predictor=YES, Level=9 | 322.6 ± 14.1 | 36.16 ± 2.41 | 1.21 ± 0.03 |
| LERC |  | 365.4 ± 14.19 | 11.83 ± 0.24 | 2.25 ± 0.07 |
| LERC_DEFLATE |  | 362.62 ± 14.48 | 15.93 ± 0.14 | 2.59 ± 0.09 |
| LERC_ZSTD |  | 363.26 ± 14.29 | 14.75 ± 0.15 | 2.27 ± 0.05 |
| LZMA |  | 351.0 ± 11.97 | 115.36 ± 2.85 | 14.03 ± 0.51 |
| LZW | Predictor=NO | 568.9 ± 16.84 | 14.92 ± 0.5 | 2.03 ± 0.05 |
| LZW | Predictor=YES | 393.12 ± 20.21 | 14.94 ± 0.46 | 1.91 ± 0.13 |
| PACKBITS |  | 512.98 ± 0.01 | 7.71 ± 0.4 | 0.26 ± 0.05 |
| ZSTD | Predictor=NO, Level=1 | 440.55 ± 6.93 | 7.65 ± 0.74 | 0.74 ± 0.07 |
| ZSTD | Predictor=NO, Level=9 | 437.81 ± 10.12 | 13.68 ± 2.36 | 0.74 ± 0.05 |
| ZSTD | Predictor=NO, Level=22 | 421.6 ± 11.53 | 284.69 ± 6.8 | 1.38 ± 0.22 |
| ZSTD | Predictor=YES, Level=1 | 363.39 ± 14.84 | 8.18 ± 0.88 | 0.73 ± 0.1 |
| ZSTD | Predictor=YES, Level=9 | 333.67 ± 16.47 | 23.18 ± 2.36 | 1.13 ± 0.12 |
| ZSTD | Predictor=YES, Level=22 | 305.77 ± 13.2 | 314.91 ± 8.7 | 1.46 ± 0.1 |



```python
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


```
