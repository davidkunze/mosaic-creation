from osgeo import gdal
import numpy as np

def create_combined_colormap(colormap_files):
    # Erstellen einer neuen leeren Colormap
    combined_colormap = gdal.ColorTable()

    # Für jede Colormap-Datei
    for colormap_file in colormap_files:
        # Colormap aus der Datei laden
        with open(colormap_file, 'r') as f:
            for line in f:
                if line.strip():  # Nur nicht-leere Zeilen verarbeiten
                    # RGB-Werte extrahieren (angenommen im Format: index,r,g,b)
                    rgb_values = list(map(int, line.strip().split(',')))
                    index = rgb_values[0]
                    r, g, b = rgb_values[1], rgb_values[2], rgb_values[3]

                    # Füge die Farbe zur kombinierten Colormap hinzu
                    combined_colormap.SetColorEntry(index, (r, g, b, 255))

    return combined_colormap

def apply_combined_colormap_to_vrt(vrt_file, combined_colormap):
    # Öffnen des VRT
    ds = gdal.Open(vrt_file)

    # Überprüfen, ob das Dataset erfolgreich geöffnet wurde
    if ds is None:
        print("Fehler beim Öffnen des VRT.")
        return
    
    # Colormap auf das erste Band anwenden
    band = ds.GetRasterBand(1)  # Annahme: Colormap für das erste Band
    band.SetColorTable(combined_colormap)
    print("Kombinierte Colormap erfolgreich angewendet.")

def create_vrt_from_tifs(tif_files, output_vrt):
    # VRT erstellen aus den TIFF-Dateien
    vrt = gdal.BuildVRT(output_vrt, tif_files)
    if vrt is None:
        print("Fehler beim Erstellen des VRT.")
    else:
        print(f"VRT erfolgreich erstellt: {output_vrt}")
    return vrt

# Beispielaufruf:
if __name__ == "__main__":
    # Liste von TIFF-Dateien
    tif_files = ['image1.tif', 'image2.tif', 'image3.tif']
    output_vrt = 'output.vrt'

    # Colormap-Dateien, die kombiniert werden sollen
    colormap_files = ['colormap1.txt', 'colormap2.txt']

    # VRT erstellen
    create_vrt_from_tifs(tif_files, output_vrt)

    # Kombinierte Colormap erstellen
    combined_colormap = create_combined_colormap(colormap_files)

    # Colormap auf das VRT anwenden
    apply_combined_colormap_to_vrt(output_vrt, combined_colormap)