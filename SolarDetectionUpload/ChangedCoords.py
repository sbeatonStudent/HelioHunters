import json
import pyproj
import rasterio
from rasterio.warp import transform
from shapely import Polygon

# # Function to convert latitude and longitude to pixel coordinates
# def latlon_to_pixel(lat, lon):
#     with rasterio.open(tiff_file) as dataset:
#         # Transform latitude and longitude to pixel coordinates ##26911/4269 is other projection system
#         col, row = transform(dataset.crs, {'init': 'EPSG:26911'},
#                              [lon], [lat])
        
#         return int(row[0]), int(col[0])

def add_offset_to_polygon(polygon, offset):
    new_coordinates = []
    for x, y in polygon.exterior.coords:
        new_coordinates.append((x + offset, y))
    return Polygon(new_coordinates)

def project_coordinates(geojson_file, source_crs, target_crs):
    # Load the GeoJSON file
    with open(geojson_file) as f:
        data = json.load(f)

    # Create a PyProj transformer for the coordinate transformation
    transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)

    # Iterate over the features and transform their coordinates
    for feature in data['features']:
        geometry = feature['geometry']
        coordinates = geometry['coordinates']

        # Transform each coordinate point
        if geometry['type'] == 'Polygon':
            coordinates = transform_polygon_coordinates(coordinates, transformer)
        elif geometry['type'] == 'MultiPolygon':
            coordinates = [transform_polygon_coordinates(polygon, transformer) for polygon in coordinates]

        # Update the transformed coordinates in the feature
        geometry['coordinates'] = coordinates

        # # Transform the centroid coordinates
        # centroid = transform_point_coordinates((feature['properties']['centroid_longitude'], feature['properties']['centroid_latitude']), transformer)
        # feature['properties']['centroid'] = centroid

    # Save the modified GeoJSON file
    with open('modified_geojson_changedcoords_big.geojson', 'w') as f:
        json.dump(data, f)


def transform_polygon_coordinates(coordinates, transformer):
    # Transform the coordinates of a polygon
    transformed_coordinates = []
    for ring in coordinates:
        transformed_ring = []
        for point in ring:
            transformed_point = transformer.transform(point[0]-0.00002, point[1])
            transformed_ring.append(transformed_point)
        transformed_coordinates.append(transformed_ring)
    return transformed_coordinates

def transform_point_coordinates(coordinates, transformer):
    # Transform the coordinates of a point
    transformed_coordinates = transformer.transform(coordinates[0]-0.00002, coordinates[1])
    return transformed_coordinates

# Usage example
source_crs = 'EPSG:4269'  # Source CRS (e.g., WGS84)
target_crs = 'EPSG:3857'  # Target CRS (e.g., Web Mercator)
tiff_file = 'data/Fresno/full_fresno.tif'
geojson_file = 'FilteredSolarOutput_Big.geojson'  # Path to the input GeoJSON file

# Read the TIFF image to get its bounds
with rasterio.open(tiff_file) as src:
    bounds = src.bounds
    target_crs = src.crs

print(target_crs)
project_coordinates(geojson_file, source_crs, target_crs)