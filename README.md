## Workflow in Python

1. Define input parameters
   - input path
   - output name ⟶ KonGEO: "bundesland_tragersystem_jahr_gebiet_datentyp_auftrageber"
   - no data value ⟶ if not 0, Null or NoData
   - output projection ⟶ EPSG:25832
2. Create subfolders 
3. Build VRT from original images
![grafik](https://github.com/davidkunze/mosaic-creation/assets/133227408/565776fc-a7c3-40ad-83f2-f1cd8508a4bf)

4. Read the metadata of the input data VRT
   - coordinate system/projection
   - number of bands
   - data type (8-bit, 16-bit...)   
5. Get the extent of the input tiles as vector data ⟶ dissolve
![grafik](https://github.com/davidkunze/mosaic-creation/assets/133227408/522086f5-789b-4a6c-845f-c760c509b808)

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
![grafik](https://github.com/davidkunze/mosaic-creation/assets/133227408/b366b805-b403-4ebf-96e4-8e82afa7937c)

9. Intersect tiles with the dissolved extent of input tiles (6.) ⟶ Remove the tiles that do not intersect
   -sdb
![grafik](https://github.com/davidkunze/mosaic-creation/assets/133227408/39004eb5-c5be-4fe3-9532-9247cb943f56)
![grafik](https://github.com/davidkunze/mosaic-creation/assets/133227408/aff56290-7e9c-4f33-90f6-f29de39e76f9)


11. Create COG tiles
12. Metadata vector files
   - Vector files from COG tile extent without no data areas
   - dissolve of the vector files without no data areas
   - vector files from COG tile extent including no data areas 
12. Appand metadata table (.csv) to metadata vector files
13. Create VRT from COG + overviews
14. Remove temporary data

  


