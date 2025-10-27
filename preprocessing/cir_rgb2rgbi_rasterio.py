import os
import rasterio
import numpy as np

# Define the folder paths for CIR and RGB images
cir_folder = r"\\lb-srv\LB-Ortho\ni\nwfva\ortho_2010\solling_nlf_fe\daten\cir\tiff"
rgb_folder = r"\\lb-srv\LB-Ortho\ni\nwfva\ortho_2010\solling_nlf_fe\daten\rgb\tiff"
output_folder = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\ni\flugzeug\2010\solling_nlf_fe\dop\daten\rohdaten"

# Get a list of all CIR images in the CIR folder
cir_images = [f for f in os.listdir(cir_folder) if f.lower().endswith('.tif')]

def merge_rgb_and_cir(rgb_image_path, cir_image_path, output_image_path):
    with rasterio.open(rgb_image_path) as rgb_src, rasterio.open(cir_image_path) as cir_src:
        # Read RGB bands (1, 2, 3)
        rgb_bands = [rgb_src.read(i) for i in (1, 2, 3)]

        # Read CIR band 2 (NIR, assuming it's the 2nd band in CIR)
        # Adjust if the NIR band is in a different position
        nir_band = cir_src.read(2)

        # Stack all four bands into one array (4, height, width)
        merged_data = np.stack(rgb_bands + [nir_band])

        # Use metadata from one of the sources, e.g., RGB image
        out_meta = rgb_src.meta.copy()
        out_meta.update({
            "count": 4,
            "dtype": merged_data.dtype,
            "driver": "GTiff"
        })

        with rasterio.open(output_image_path, "w", **out_meta) as dest:
            dest.write(merged_data)

# Iterate over each CIR image
for cir_image_name in cir_images:
    base_filename = os.path.splitext(cir_image_name)[0]
    rgb_image_name = 'ef' + base_filename[3:] + ".tif"

    cir_image_path = os.path.join(cir_folder, cir_image_name)
    rgb_image_path = os.path.join(rgb_folder, rgb_image_name)
    output_image_path = os.path.join(output_folder, base_filename + "_rgbi.tif")

    if os.path.exists(rgb_image_path):  # Check to avoid errors if RGB image is missing
        print(f"Merging:\n  RGB: {rgb_image_path}\n  CIR: {cir_image_path}")
        merge_rgb_and_cir(rgb_image_path, cir_image_path, output_image_path)
    else:
        print(f"RGB file not found for {cir_image_name}")
