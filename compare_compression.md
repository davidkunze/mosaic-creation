# Compression Performance Comparison

<script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
<table class="sortable">
<thead>
<tr><th>Input File</th><th>Method</th><th>Predictor</th><th>Format</th><th>Type</th><th>Size (MB)</th><th>Write Time (s)</th><th>Read Time (s)</th></tr>
</thead>
<tbody>
<tr><td>588000_5728000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>800.00</td><td>-</td><td>2.82</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>98.57</td><td>9.62</td><td>0.87</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>92.09</td><td>10.22</td><td>1.13</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>66.13</td><td>9.51</td><td>1.05</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>64.39</td><td>11.52</td><td>0.98</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>87.20</td><td>7.04</td><td>0.80</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>67.11</td><td>7.96</td><td>1.11</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>64.34</td><td>8.65</td><td>1.20</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>64.73</td><td>8.59</td><td>1.12</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>1078.01</td><td>7.50</td><td>0.92</td></tr>
<tr><td>588000_5728000_16Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>68.40</td><td>38.56</td><td>5.46</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>400.01</td><td>-</td><td>1.86</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>40.24</td><td>6.23</td><td>0.39</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>26.53</td><td>6.57</td><td>0.53</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>22.99</td><td>6.48</td><td>0.46</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>21.59</td><td>9.06</td><td>0.42</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>43.63</td><td>5.06</td><td>0.37</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>27.77</td><td>6.36</td><td>0.67</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>25.63</td><td>6.66</td><td>0.70</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>25.71</td><td>6.81</td><td>0.63</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>539.01</td><td>5.19</td><td>0.25</td></tr>
<tr><td>588000_5728000_8Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>24.08</td><td>21.92</td><td>2.74</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>800.00</td><td>-</td><td>0.62</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>467.82</td><td>12.74</td><td>1.79</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>424.41</td><td>14.43</td><td>2.02</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>309.77</td><td>14.00</td><td>1.52</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>308.26</td><td>13.40</td><td>1.19</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>363.46</td><td>8.94</td><td>0.80</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>307.81</td><td>10.27</td><td>1.48</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>303.66</td><td>14.11</td><td>2.06</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>305.04</td><td>12.15</td><td>1.52</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>1078.01</td><td>8.83</td><td>0.69</td></tr>
<tr><td>590000_5724000_16Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>327.35</td><td>91.71</td><td>13.88</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>400.01</td><td>-</td><td>1.83</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>173.04</td><td>8.44</td><td>0.72</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>104.55</td><td>8.69</td><td>0.73</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>92.87</td><td>10.79</td><td>0.54</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>89.51</td><td>13.99</td><td>0.50</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>181.76</td><td>6.36</td><td>0.26</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>107.64</td><td>8.77</td><td>1.05</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>104.97</td><td>9.99</td><td>1.20</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>105.34</td><td>9.92</td><td>1.15</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>539.01</td><td>5.82</td><td>0.31</td></tr>
<tr><td>590000_5724000_8Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>98.79</td><td>52.72</td><td>5.44</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>800.00</td><td>-</td><td>3.56</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>1231.14</td><td>19.00</td><td>3.20</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>1135.82</td><td>22.58</td><td>3.76</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>823.10</td><td>21.36</td><td>2.38</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>821.68</td><td>15.44</td><td>1.82</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>922.03</td><td>12.64</td><td>0.95</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>824.80</td><td>14.28</td><td>2.22</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>819.84</td><td>24.61</td><td>3.47</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>823.43</td><td>18.24</td><td>2.33</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>1078.01</td><td>9.89</td><td>0.79</td></tr>
<tr><td>590000_5726000_16Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>872.41</td><td>194.61</td><td>31.16</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>GTiff</td><td>Lossless</td><td>400.01</td><td>-</td><td>1.74</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>uncompressed</td><td>N/A</td><td>COG</td><td>Lossless</td><td>489.97</td><td>12.28</td><td>1.83</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>LZW</td><td>2</td><td>COG</td><td>Lossless</td><td>307.18</td><td>12.02</td><td>1.56</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>DEFLATE</td><td>2</td><td>COG</td><td>Lossless</td><td>266.71</td><td>15.77</td><td>1.03</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>ZSTD</td><td>2</td><td>COG</td><td>Lossless</td><td>261.41</td><td>21.10</td><td>0.95</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>PACKBITS</td><td>N/A</td><td>COG</td><td>Lossless</td><td>461.04</td><td>8.46</td><td>0.25</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>LERC</td><td>N/A</td><td>COG</td><td>Lossy</td><td>297.85</td><td>12.24</td><td>2.11</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>LERC_DEFLATE</td><td>N/A</td><td>COG</td><td>Lossy</td><td>294.41</td><td>15.62</td><td>2.47</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>LERC_ZSTD</td><td>N/A</td><td>COG</td><td>Lossy</td><td>294.87</td><td>14.86</td><td>2.30</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>JPEG2000</td><td>N/A</td><td>COG</td><td>Lossy</td><td>539.01</td><td>6.94</td><td>0.46</td></tr>
<tr><td>590000_5726000_8Bit.tif</td><td>LZMA</td><td>N/A</td><td>COG</td><td>Lossless</td><td>291.32</td><td>108.86</td><td>12.09</td></tr>
</tbody>
</table>



| Input File | Method | Predictor | Format | Type | Size (MB) | Write Time (s) | Read Time (s) |
|------------|--------|-----------|--------|------|----------|--------------|--------------|
| 616000_5740000_16bit.tif | uncompressed | N/A | GTiff | Lossless | 800.00 | - | 3.83 |
| 616000_5740000_16bit.tif | uncompressed | N/A | COG | Lossless | 1369.08 | 20.78 | 3.79 |
| 616000_5740000_16bit.tif | LZW | 2 | COG | Lossless | 1296.76 | 25.48 | 4.31 |
| 616000_5740000_16bit.tif | DEFLATE | 2 | COG | Lossless | 935.78 | 23.75 | 2.76 |
| 616000_5740000_16bit.tif | ZSTD | 2 | COG | Lossless | 934.86 | 17.06 | 2.36 |
| 616000_5740000_16bit.tif | PACKBITS | N/A | COG | Lossless | 1025.75 | 13.39 | 0.89 |
| 616000_5740000_16bit.tif | LERC | N/A | COG | Lossless with -co QUALITY=100 | 950.67 | 15.95 | 2.67 |
| 616000_5740000_16bit.tif | LERC_DEFLATE | N/A | COG | Lossless with -co QUALITY=100 | 946.69 | 26.95 | 3.78 |
| 616000_5740000_16bit.tif | LERC_ZSTD | N/A | COG | Lossless with -co QUALITY=100 | 950.28 | 19.43 | 2.57 |
| 616000_5740000_16bit.tif | JPEG2000 | N/A | COG | Lossless with -co QUALITY=100 | 1078.01 | 10.22 | 0.90 |
| 616000_5740000_16bit.tif | LZMA | N/A | COG | Lossless | 974.26 | 211.45 | 36.65 |
| 616000_5740000_8bit.tif | uncompressed | N/A | GTiff | Lossless | 400.01 | - | 1.76 |
| 616000_5740000_8bit.tif | uncompressed | N/A | COG | Lossless | 578.36 | 9.10 | 2.22 |
| 616000_5740000_8bit.tif | LZW | 2 | COG | Lossless | 393.53 | 8.45 | 2.10 |
| 616000_5740000_8bit.tif | DEFLATE | 2 | COG | Lossless | 333.17 | 11.25 | 1.46 |
| 616000_5740000_8bit.tif | ZSTD | 2 | COG | Lossless | 333.44 | 17.18 | 1.38 |
| 616000_5740000_8bit.tif | PACKBITS | N/A | COG | Lossless | 512.50 | 4.38 | 0.39 |
| 616000_5740000_8bit.tif | LERC | N/A | COG | Lossless with -co QUALITY=100 | 365.49 | 8.16 | 2.39 |
| 616000_5740000_8bit.tif | LERC_DEFLATE | N/A | COG | Lossless with -co QUALITY=100 | 362.81 | 12.48 | 2.71 |
| 616000_5740000_8bit.tif | LERC_ZSTD | N/A | COG | Lossless with -co QUALITY=100 | 363.42 | 11.41 | 2.31 |
| 616000_5740000_8bit.tif | JPEG2000 | N/A | COG | Lossless with -co QUALITY=100 | 538.01 | 1.86 | 0.34 |
| 616000_5740000_8bit.tif | LZMA | N/A | COG | Lossless | 356.72 | 111.39 | 15.34 |

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
    "WEBP": ("Lossless with -co QUALITY=100", [None]),  # WEBP Lossless enabled
    "LERC": ("Lossless with -co QUALITY=100", [None]),  # LERC is lossy unless -co QUALITY=100
    "LERC_DEFLATE": ("Lossless with -co QUALITY=100", [None]),  # LERC_DEFLATE is also lossy unless -co QUALITY=100
    "LERC_ZSTD": ("Lossless with -co QUALITY=100", [None]),  # LERC_ZSTD is lossy unless -co QUALITY=100
    "JPEG2000": ("Lossless with -co QUALITY=100", [None]),  # JPEG2000 can be lossless, but default is lossy
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
        options.append("-co QUALITY=100")

    if compression == "JPEG2000":
        options.append("-co QUALITY=100")  # Enforce lossless JPEG2000

    if compression in ["LERC", "LERC_DEFLATE", "LERC_ZSTD"]:
        options.append("-co QUALITY=100")  # Ensure LERC is lossless

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
