import geopandas as gpd
import numpy
import fiona
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid  # this is from shapely, not pandas

# get_angle function
def get_angles(vec_1, vec_2):
    # Return the angle, in degrees, between two vectors
    # Convert 2D vectors to 3D by adding a 0 in the third dimension
    vec_1_3d = numpy.array([vec_1[0], vec_1[1], 0])
    vec_2_3d = numpy.array([vec_2[0], vec_2[1], 0])
    dot = numpy.dot(vec_1_3d, vec_2_3d)
    det = numpy.cross(vec_1_3d, vec_2_3d)[2]  # Take the z-component of the cross product
    angle_in_rad = numpy.arctan2(det, dot)
    return numpy.degrees(angle_in_rad)

# Function for removing superfluous corner points along a straight line that would require a large amount of memory space
def simplify_by_angle(poly_in, deg_tol=1):
    # poly_in: shapely Polygon
    # deg_tol: degree tolerance for comparison between successive vectors
    ext_poly_coords = poly_in.exterior.coords[:]
    vector_rep = numpy.diff(ext_poly_coords, axis=0)
    num_vectors = len(vector_rep)
    angles_list = []
    for i in range(0, num_vectors):
        angles_list.append(numpy.abs(get_angles(vector_rep[i], vector_rep[(i + 1) % num_vectors])))
    # get mask satisfying tolerance
    thresh_vals_by_deg = numpy.where(numpy.array(angles_list) > deg_tol)
    new_idx = list(thresh_vals_by_deg[0] + 1)
    new_vertices = [ext_poly_coords[idx] for idx in new_idx]
    return Polygon(new_vertices)

def remove_inner_rings(geom):
    if isinstance(geom, Polygon):
        geom = simplify_by_angle(geom)
        return Polygon(geom.exterior)
    elif isinstance(geom, MultiPolygon):
        geom = MultiPolygon([simplify_by_angle(p) for p in geom.geoms])
        return MultiPolygon([Polygon(p.exterior) for p in geom.geoms])
    else:
        return geom

input_file = r"\\lb-srv\LB-Projekte\fernerkundung\luftbild\he\flugzeug\2020\muenzenberg_sgb2\dop\daten\rohdaten\ortho_muenzenberg_2020_removenodata_cutline.gpkg"

# Load GeoPackage
layernames = fiona.listlayers(input_file)
gdf = gpd.read_file(input_file, layer=layernames[0])
gdf["geometry"] = gdf["geometry"].apply(remove_inner_rings).apply(make_valid).apply(remove_inner_rings)

# Apply the inner ring removal
# Save to new file
output_file = input_file.replace('.gpkg', '_noinnerrings.gpkg')
gdf.to_file(output_file, driver="GPKG", layer = layernames[0])
