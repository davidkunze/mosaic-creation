

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
    "WEBP": ("Lossless", [None]),
    "LZW": ("Lossless", [2]),
    "DEFLATE": ("Lossless", [2]),
    "ZSTD": ("Lossless", [2]),
    "PACKBITS": ("Lossless", [None]),
    "LERC": ("Lossy", [None]),
    "LERC_DEFLATE": ("Lossless", [None]),
    "LERC_ZSTD": ("Lossless", [None]),
    "JPEG2000": ("Lossless", [None]),
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
    return None

def compress_raster(input_file, output_file, compression=None, predictor=None):
    """Compress raster using gdal_translate with COG format."""
    options = ["-of COG"]

    if compression:
        options.append(f"-co COMPRESS={compression}")
    if predictor:
        options.append(f"-co PREDICTOR={predictor}")
    if compression in ["WEBP","LERC", "LERC_DEFLATE", "LERC_ZSTD","JPEG2000"]:
        options.append("-co QUALITY=100")

    command = f'gdal_translate {" ".join(options)} "{input_file}" "{output_file}"'
    print(command)

    start_time = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
        return round(time.time() - start_time, 2)
    except subprocess.CalledProcessError:
        print(f"❌ Error compressing {input_file} with {compression if compression else 'NO COMPRESSION'}")
        return None

# Store results for markdown output
results = []

# Process each input raster
for input_raster in input_rasters:
    original_size = get_file_size(input_raster)
    original_read_time = measure_read_time(input_raster)

    results.append((
        os.path.basename(input_raster), "uncompressed", "N/A", "GTiff", "Lossless",
        round(original_size, 2), "-", original_read_time
    ))

    cog_uncompressed_filename = f"{os.path.splitext(os.path.basename(input_raster))[0]}_COG.tif"
    cog_uncompressed_file = os.path.join(output_folder, cog_uncompressed_filename)

    cog_write_time = compress_raster(input_raster, cog_uncompressed_file)
    if cog_write_time is not None:
        cog_read_time = measure_read_time(cog_uncompressed_file)
        cog_size = get_file_size(cog_uncompressed_file)

        results.append((
            os.path.basename(input_raster), "uncompressed", "N/A", "COG", "Lossless",
            round(cog_size, 2), cog_write_time, cog_read_time
        ))

    for compression, (comp_type, predictors) in compression_methods.items():
        for predictor in predictors:
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


# # Write results to Markdown file with sortable table
# with open(output_md, "w") as md_file:
#     md_file.write("# Compression Performance Comparison\n\n")
#     md_file.write('<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>\n')
#     md_file.write('<table class="sortable">\n')
#     md_file.write("<thead>\n")
#     md_file.write("<tr><th>Input File</th><th>Method</th><th>Predictor</th><th>Format</th><th>Type</th>"
#                   "<th>Size (MB)</th><th>Write Time (s)</th><th>Read Time (s)</th></tr>\n")
#     md_file.write("</thead>\n<tbody>\n")
    
#     for file, comp, pred, fmt, comp_type, size, write_t, read_t in results:
#         write_t_str = f"{write_t:.2f}" if isinstance(write_t, (int, float)) else write_t
#         read_t_str = f"{read_t:.2f}" if isinstance(read_t, (int, float)) else "Error"
        
#         md_file.write(f"<tr><td>{file}</td><td>{comp}</td><td>{pred}</td><td>{fmt}</td><td>{comp_type}</td>"
#                       f"<td>{size:.2f}</td><td>{write_t_str}</td><td>{read_t_str}</td></tr>\n")

#     md_file.write("</tbody>\n</table>\n")

# print(f"\n✅ Results saved to {output_md}")


```
