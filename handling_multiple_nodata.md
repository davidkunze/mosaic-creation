python

from osgeo import gdal
import numpy as np

input_path = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\ni\flugzeug\2006\harz_np\dop\daten\ni_flugzeug_2006_harz_np_dop.vrt" 
output_path = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\ni\flugzeug\2006\harz_np\dop\daten\mask_254_254_254_2.tif"

dataset = gdal.Open(input_path)
driver = gdal.GetDriverByName("GTiff")

# Create output raster
out_ds = driver.Create(
    output_path,
    dataset.RasterXSize,
    dataset.RasterYSize,
    1,
    gdal.GDT_Byte,
    options=["TILED=YES", "COMPRESS=DEFLATE"]
)
out_ds.SetGeoTransform(dataset.GetGeoTransform())
out_ds.SetProjection(dataset.GetProjection())

# Define tile size
block_size = 1024

for y in range(0, dataset.RasterYSize, block_size):
    rows = min(block_size, dataset.RasterYSize - y)
    for x in range(0, dataset.RasterXSize, block_size):
        cols = min(block_size, dataset.RasterXSize - x)

        # Read the window from each band
        r = dataset.GetRasterBand(1).ReadAsArray(x, y, cols, rows)
        g = dataset.GetRasterBand(2).ReadAsArray(x, y, cols, rows)
        b = dataset.GetRasterBand(3).ReadAsArray(x, y, cols, rows)

        # Build the mask
        mask = ((r == 254) & (g == 254) & (b == 254)).astype(np.uint8)

        # Write to output
        out_ds.GetRasterBand(1).WriteArray(mask, x, y)

print(f"Mask saved to {output_path}")
