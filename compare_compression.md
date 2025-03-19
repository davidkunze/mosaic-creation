# Compression Performance Comparison

| Input File | Method | Predictor | Format | Type | Size (MB) | Write Time (s) | Read Time (s) |
|------------|--------|-----------|--------|------|----------|--------------|--------------|
| 616000_5740000_16bit.tif | uncompressed | N/A | GTiff | Lossless | 800.00 | - | 3.78 |
| 616000_5740000_16bit.tif | uncompressed | N/A | COG | Lossless | 1369.08 | 19.62 | 3.74 |
| 616000_5740000_16bit.tif | LZW | 2 | COG | Lossless | 1296.76 | 23.96 | 4.30 |
| 616000_5740000_16bit.tif | DEFLATE | 2 | COG | Lossless | 935.78 | 22.53 | 2.78 |
| 616000_5740000_16bit.tif | ZSTD | 2 | COG | Lossless | 934.86 | 16.19 | 2.11 |
| 616000_5740000_16bit.tif | PACKBITS | N/A | COG | Lossless | 1025.75 | 12.66 | 1.18 |
| 616000_5740000_16bit.tif | LERC | N/A | COG | Lossless | 950.67 | 15.11 | 2.66 |
| 616000_5740000_16bit.tif | LERC_DEFLATE | N/A | COG | Lossless | 946.69 | 26.65 | 3.77 |
| 616000_5740000_16bit.tif | LERC_ZSTD | N/A | COG | Lossless | 950.28 | 19.34 | 2.57 |
| 616000_5740000_16bit.tif | JPEG2000 | N/A | COG | Lossless | 1078.01 | 9.94 | 1.01 |
| 616000_5740000_16bit.tif | LZMA | N/A | COG | Lossless | 974.26 | 212.08 | 36.37 |
| 616000_5740000_8bit.tif | uncompressed | N/A | GTiff | Lossless | 400.01 | - | 1.74 |
| 616000_5740000_8bit.tif | uncompressed | N/A | COG | Lossless | 576.26 | 11.71 | 2.15 |
| 616000_5740000_8bit.tif | LZW | 2 | COG | Lossless | 383.92 | 11.93 | 1.99 |
| 616000_5740000_8bit.tif | DEFLATE | 2 | COG | Lossless | 327.03 | 14.67 | 1.38 |
| 616000_5740000_8bit.tif | ZSTD | 2 | COG | Lossless | 326.47 | 20.59 | 1.13 |
| 616000_5740000_8bit.tif | PACKBITS | N/A | COG | Lossless | 512.88 | 7.76 | 0.37 |
| 616000_5740000_8bit.tif | LERC | N/A | COG | Lossless | 358.97 | 11.68 | 2.44 |
| 616000_5740000_8bit.tif | LERC_DEFLATE | N/A | COG | Lossless | 356.27 | 16.06 | 2.69 |
| 616000_5740000_8bit.tif | LERC_ZSTD | N/A | COG | Lossless | 356.88 | 14.86 | 2.35 |
| 616000_5740000_8bit.tif | JPEG2000 | N/A | COG | Lossless | 539.01 | 6.47 | 0.43 |
| 616000_5740000_8bit.tif | LZMA | N/A | COG | Lossless | 354.05 | 114.08 | 15.31 |


```python
import os
import glob
import time
import subprocess
from osgeo import gdal

# Directories for input and output files
input_folder = r'D:\Test\test_compression\daten'
output_folder = r'D:\Test\test_compression\results'
output_md = os.path.join(output_folder, "results.md")  # Markdown output file

# Scan for input raster files
input_rasters = glob.glob(os.path.join(input_folder, '*.tif'))

# Compression methods with their types (Lossless/Lossy)
compression_methods = {
    "LZW": ("Lossless", [2]),
    "DEFLATE": ("Lossless", [2]),
    "ZSTD": ("Lossless", [2]),
    "PACKBITS": ("Lossless", [None]),
    "WEBP": ("Lossless", [None]),  # WEBP Lossless enabled
    "LERC": ("Lossless", [None]),  # LERC is lossy unless MAX_Z_ERROR=0
    "LERC_DEFLATE": ("Lossless", [None]),  # LERC_DEFLATE is also lossy unless MAX_Z_ERROR=0
    "LERC_ZSTD": ("Lossless", [None]),  # LERC_ZSTD is lossy unless MAX_Z_ERROR=0
    "JPEG2000": ("Lossless", [None]),  # JPEG2000 can be lossless, but default is lossy
    "LZMA": ("Lossless", [None])
}

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
    return None  # Indicate failure

def compress_raster(input_file, output_file, compression=None, predictor=None):
    """
    Compress raster using gdal_translate with COG format.
    """
    options = ["-of COG"]

    if compression:
        options.append(f"-co COMPRESS={compression}")

    if predictor:
        options.append(f"-co PREDICTOR={predictor}")

    # Special cases for specific formats
    if compression == "WEBP":
        options.append("-co LOSSLESS=TRUE")

    if compression == "JPEG2000":
        options.append("-co QUALITY=100")  # Enforce lossless JPEG2000

    if compression in ["LERC", "LERC_DEFLATE", "LERC_ZSTD"]:
        options.append("-co MAX_Z_ERROR=0")  # Ensure LERC is lossless

    # Build and run command
    command = f'gdal_translate {" ".join(options)} "{input_file}" "{output_file}"'
    print(command)

    start_time = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
        return round(time.time() - start_time, 2)  # Return compression time (rounded)
    except subprocess.CalledProcessError:
        print(f"❌ Error compressing {input_file} with {compression if compression else 'NO COMPRESSION'}")
        return None

# Store results for markdown output
results = []

# Process each input raster
for input_raster in input_rasters:
    # Original GTiff file stats
    original_size = get_file_size(input_raster)
    original_read_time = measure_read_time(input_raster)

    # Store original GTiff in table
    results.append((
        os.path.basename(input_raster), "uncompressed", "N/A", "GTiff", "Lossless",
        round(original_size, 2), "-", original_read_time
    ))

    # Generate an uncompressed COG
    cog_uncompressed_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_COG.tif"
    cog_uncompressed_file = os.path.join(output_folder, cog_uncompressed_filename)

    cog_write_time = compress_raster(input_raster, cog_uncompressed_file)
    if cog_write_time is not None:
        cog_read_time = measure_read_time(cog_uncompressed_file)
        cog_size = get_file_size(cog_uncompressed_file)

        # Store COG uncompressed stats
        results.append((
            os.path.basename(input_raster), "uncompressed", "N/A", "COG", "Lossless",
            round(cog_size, 2), cog_write_time, cog_read_time
        ))

    # Loop through compression methods
    for compression, (comp_type, predictors) in compression_methods.items():
        for predictor in predictors:
            # Generate COG compressed version
            cog_output_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_{compression}_COG.tif"
            cog_output_file = os.path.join(output_folder, cog_output_filename)

            cog_write_time = compress_raster(input_raster, cog_output_file, compression, predictor)
            if cog_write_time is None:
                continue

            cog_read_time = measure_read_time(cog_output_file)
            cog_file_size = get_file_size(cog_output_file)

            results.append((
                os.path.basename(input_raster), compression, predictor if predictor else "N/A",
                "COG", comp_type, round(cog_file_size, 2), cog_write_time, cog_read_time
            ))

# Write results to Markdown file
with open(output_md, "w") as md_file:
    md_file.write("# Compression Performance Comparison\n\n")
    md_file.write("| Input File | Method | Predictor | Format | Type | Size (MB) | Write Time (s) | Read Time (s) |\n")
    md_file.write("|------------|--------|-----------|--------|------|----------|--------------|--------------|\n")
    
    for file, comp, pred, fmt, comp_type, size, write_t, read_t in results:
        write_t_str = f"{write_t:.2f}" if isinstance(write_t, (int, float)) else write_t  # Keep "-" for uncompressed
        read_t_str = f"{read_t:.2f}" if isinstance(read_t, (int, float)) else "Error"
        
        md_file.write(f"| {file} | {comp} | {pred} | {fmt} | {comp_type} | {size:.2f} | {write_t_str} | {read_t_str} |\n")

print(f"\n✅ Results saved to {output_md}")

```
