import geopandas as gpd
import rasterio
from shapely.geometry import Polygon, shape, box

# Paths to input GeoJSON file, TIFF image, and output GeoJSON file
geojson_file = 'SolarArrayPolygons.geojson'
filepath = 'data/'
tiff_files = ['full_fresno', 'm_3712106_ne_10_060_20220621', 'm_3712106_nw_10_060_20220621', 'm_3712106_se_10_060_20220621', 'm_3712107_nw_10_060_20220621', 'm_3812162_se_10_060_20220621', 'm_3812162_sw_10_060_20220621']
output_file = 'FilteredSolarOutput_Big.geojson'

# Filter polygons that intersect with the TIFF image bounds
filtered_polygons = []

for file in tiff_files:
    # Read the GeoJSON file
    gdf = gpd.read_file(geojson_file)
    
    # Read the TIFF image to get its bounds
    tiff_file = filepath + file + '.tif'
    with rasterio.open(tiff_file) as src:
        bounds = src.bounds
        crs = src.crs

    print(crs)
    # Convert the bounds to a Polygon
    tif_polygon = box(bounds.left, bounds.bottom, bounds.right, bounds.top)

    print(tif_polygon)


    for idx, row in gdf.iterrows():
        polygon = Polygon(row['geometry'])
        gdf = gpd.GeoDataFrame(geometry=[polygon], crs='EPSG:4269')
        gdf = gdf.to_crs(crs)
        if tif_polygon.contains(gdf.geometry.all()):
            updated_row = row.copy()
            updated_row['image_name'] = file
            filtered_polygons.append(updated_row)
    
    print('end')

# Create a new GeoDataFrame with the filtered polygons
filtered_gdf = gpd.GeoDataFrame(filtered_polygons, crs=gdf.crs)

# Export the filtered GeoJSON file
filtered_gdf.to_file(output_file, driver='GeoJSON')


