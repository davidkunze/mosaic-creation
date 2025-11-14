import os
import geopandas as gpd
import fiona
import subprocess

def find_extent_files(path, suffix, no_suffix=False):
    results = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix) and not file.endswith(no_suffix):
                    results.append(os.path.join(root, file))
    return results

folder = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild"
extent_files = find_extent_files(folder, "_extent.gpkg","inputdata_extent.gpkg")

# Output
for file in extent_files:
    print(file)

print(f"\nFound files: {len(extent_files)}")


pg_conn = 'PG:"dbname=orthophotos user=postgres password=postgres host=localhost port=5432 ACTIVE_SCHEMA=tiles"'

# cmd_list = []
# for gpkg in extent_files[:3]:
#     gpkg_name = os.path.basename(gpkg)
#     print(f"\n=== Importiere {gpkg_name} ===")

#     # Alle Layer im GeoPackage auslesen
#     layers = fiona.listlayers(gpkg)
#     print(f"  Layers: {', '.join(layers)}")

#     for layer in layers:
#         # ogr2ogr-Befehl
#         cmd = f'ogr2ogr -f "PostgreSQL" {pg_conn} "{gpkg}" {layer} ' \
#               f'-nln tiles.{layer} ' \
#               f'-nlt PROMOTE_TO_MULTI '

#         cmd_list.append(cmd)

#         # result = subprocess.run(cmd)

batch_file = r"Y:\David\vrt_cog\skripte\import_ogr2ogr.bat"

with open(batch_file, "w", encoding="utf-8") as f:
    # Write batch file header
    f.write("@echo off\n") 
    f.write("REM === Import GeoPackages to PostGIS ===\n\n")

    # (Optional) load OSGeo4W environment if needed
    f.write("CALL \"C:\\Program Files\\QGIS 3.40.9\\OSGeo4W.bat\"\n\n") # not needed if you run in OSGeo4W Shell

    for gpkg in extent_files:
        gpkg_name = os.path.basename(gpkg)
        layers = fiona.listlayers(gpkg)
        for layer in layers:
            cmd = (
                f'ogr2ogr -f "PostgreSQL" {pg_conn} "{gpkg}" {layer} '
                f'-nln tiles.{layer} -nlt PROMOTE_TO_MULTI\n'
            )
            f.write(cmd)
        f.write("\n")
    f.write("echo.\necho ✅ All imports finished!\npause\n")

subprocess.run(batch_file)