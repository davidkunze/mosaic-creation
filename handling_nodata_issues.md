Pixels that contain the nodata value in a band are incorrectly regarded as nodata pixels and are displayed transparently in most GIS systems.
example: cir aerial image with OSM in backgroud, nodata value: 254
![grafik](https://github.com/user-attachments/assets/16ed7fb1-c4d3-429c-b58b-500ab0200238)


1. create nodata raster mask with specific value

```python
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
```
![grafik](https://github.com/user-attachments/assets/567c1dbc-372d-4e0a-b9e3-c47ad521b35b)

2. convert raster to polygon with OSgeo4W Shell:
```
gdal_contour -fl 1 -b 1 -f "GPKG" -p mask_254_254_254_2.tif mask.gpkg
```
![grafik](https://github.com/user-attachments/assets/15a7b1d5-d385-4de2-98e8-b0e693e97128)

3. manual adjustment in QGIS
example:
- multipart to singlepart:
- remove outside nodata polygon
- dissolve remaining polygons
- 
![grafik](https://github.com/user-attachments/assets/6a9ef1cc-67ef-4f4e-be95-38e72e74b8b9)
