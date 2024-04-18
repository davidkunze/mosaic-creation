## Workflow in Python

1. Define input parameters
   - input path
   - output name ⟶ KonGEO: "bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber"
   - no data value ⟶ if not 0, Null or NoData
   - output projection ⟶ EPSG:25832
2. Create subfolders 
3. Build VRT from original images
4. Read the metadata of the input data VRT
   - coordinate system/projection
   - number of bands
   - data type (8-bit, 16-bit...)   
5. Get the extent of the input tiles as vector data ⟶ dissolve
6. If EPSG is not 25832 reprojection of the VRT and extent vector data
7. Read the metadata of the reprojected VRT
   - resolution
   - raster origin
   - raster width
   - raster hight
8. Split VRT extent into tiles
   - Tile size: 2000 x 2000 m
   - easting/northing of the lower left corner: even thousand (e.g. 614000 x 5782000)
   - write into tile extents into a list
9. Intersect tiles with the dissolved extent of input tiles (6.) ⟶ Remove the tiles that do not intersect
10. Create COG tiles
11. Metadata vector files
   - Vector files from COG tile extent without no data areas
   - dissolve of the vector files without no data areas
   - vector files from COG tile extent including no data areas 
12. Appand metadata table (.csv) to metadata vector files
13. Create VRT from COG + overviews
14. Remove temporary data

  


