import json
import rasterio
from rasterio.warp import transform

# Path to the TIFF file
tif_path = 'data/Fresno/full_fresno.tif'

# Function to convert latitude and longitude to pixel coordinates
def latlon_to_pixel(lat, lon):
    with rasterio.open(tif_path) as dataset:
        # Transform latitude and longitude to pixel coordinates ##26911/4269 is other projection system
        col, row = transform(dataset.crs, {'init': 'EPSG:26911'},
                             [lon], [lat])
        
        return int(row[0]), int(col[0])

# Load GEOJSON
with open('modified_geojson_changedcoords.geojson') as geojson_file:
    geojson_data = json.load(geojson_file)

# Iterate through features and transform pixel coordinates
for feature in geojson_data['features']:
    # Get the pixel vertices
    vertices_pixels = feature['properties']['polygon_vertices_pixels']
    
    # Transform each vertex
    transformed_vertices = []
    for vertex in vertices_pixels:
        lat, lon = vertex
        row, col = latlon_to_pixel(lat, lon)
        transformed_vertices.append([row, col])
    
    # Update the transformed vertices in the feature properties
    feature['properties']['polygon_vertices_pixels'] = transformed_vertices

# Save the updated GEOJSON
with open('new_pixels_panels.geojson', 'w') as output_file:
    json.dump(geojson_data, output_file)