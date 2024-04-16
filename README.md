## Workflow in Python

1. Define input parameters
   - input path
   - output name ⟶ KonGEO: "bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber"
   - nodata value ⟶ if not 0, Null or NoData
   - output projection
3. Create subfolders 
4. Build VRT from original images
5. Read metadata of the input data
7. gdaltindex
8. Split VRT into tiles
   - Tile size: 2000 x 2000 m
   - easting/northing of the lower left corner: even thousand (e.g. 614000 x 5782000)
   - name: prefix_llx_lly.tif (e.g. cog_614000_5782000.tif)
   - 
   **- reproject**   

