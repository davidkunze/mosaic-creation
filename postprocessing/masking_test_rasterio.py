
import rasterio
import numpy as np
from rasterio.shutil import copy as rio_copy
from rasterio.enums import Resampling
from rasterio.io import MemoryFile

# === Parameter ===
input_path = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\he\flugzeug\2020\muenzenberg_sgb2\dop\testdaten\daten\kacheln\he_flugzeug_2020_muenzenberg_sgb2_dop_484000_5580000_clip.tif"
output_path = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\he\flugzeug\2020\muenzenberg_sgb2\dop\testdaten\daten\kacheln\he_flugzeug_2020_muenzenberg_sgb2_dop_484000_5580000_clip_mask.tif"
nodata_val = 65535

# === Schritt 1: Raster einlesen ===
with rasterio.open(input_path) as src:
    data = src.read()  # shape: (bands, rows, cols)
    profile = src.profile.copy()
    count, height, width = data.shape

    # Maske: True = Zelle ist NODATA in allen Bändern
    mask = np.all(data == nodata_val, axis=0).astype("uint8")  # shape: (rows, cols), dtype=uint8
    # 0 = masked (nodata), 255 = valid
    internal_mask = np.where(mask, 0, 255).astype("uint8")

# === Schritt 2: Temporäres GeoTIFF mit interner Maske erzeugen ===
profile.pop("nodata", None)
profile.update({
    "compress": "DEFLATE",
    "tiled": True,
    "blockxsize": 512,
    "blockysize": 512,
    "driver": "GTiff"
})

with MemoryFile() as memfile:
    with memfile.open(**profile) as dst:
        dst.write(data)
        dst.write_mask(internal_mask)

    # === Schritt 3: In COG konvertieren ===
    rio_copy(
        memfile.name,
        output_path,
        driver="COG",
        compress="ZSTD",
        resampling="nearest"
    )


# with rasterio.open(output_path) as src:
#     data = src.read()
#     profile = src.profile.copy()

# masked_data = np.where(internal_mask == 0, -9999, data[4])

# from rasterio import open
# from rasterio.transform import from_origin

# profile.update({
#     "count": 1,
#     "dtype": "int32",       # falls du -9999 brauchst
#     "nodata": -9999,
# })
# masked_tif = output_path.replace(".tif", "_masked.tif")
# with open(masked_tif, "w", **profile) as dst:
#     dst.write(masked_data, 1)

# gdalcontString = f'gdal_contour -b 1 -fl 1 -snodata -9999 -f {masked_tif}'
# subprocess.run(gdalcontString)


import rasterio
import numpy as np
import subprocess

output_path = "pfad/zur/deiner_datei.tif"
nodata_val = -9999

# 1. Datei öffnen und 5. Band lesen
with rasterio.open(output_path) as src:
    data = src.read()
    internal_mask = src.read_masks(1)  # Oder eigenes Maskenarray laden
    profile = src.profile.copy()

# 2. Maskierung anwenden
masked_data = np.where(internal_mask == 0, nodata_val, data[4])  # Index 4 = 5. Band

# 3. Neues Profil für Einzelband mit Nodata
profile.update({
    "count": 1,
    "dtype": "int32",
    "nodata": nodata_val
})

# 4. Schreiben
masked_tif = output_path.replace(".tif", "_masked.tif")
with rasterio.open(masked_tif, "w", **profile) as dst:
    dst.write(masked_data, 1)

# 5. Kontur erzeugen
gdal_output = masked_tif.replace(".tif", "_contours.gpkg")
gdalcontString = f'gdal_contour -b 1 -fl 1 -snodata {nodata_val} -f GPKG "{masked_tif}" "{gdal_output}"'
subprocess.run(gdalcontString, shell=True)

print("✅ Konturen erstellt:", gdal_output)
