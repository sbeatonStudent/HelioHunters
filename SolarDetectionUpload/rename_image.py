import json

# Load the GeoJSON file
with open('FilteredSolarOutput.geojson') as f:
    geojson_data = json.load(f)

# Modify the image names
for feature in geojson_data['features']:
    feature['properties']['image_name'] = 'full_fresno'

# Export the modified GeoJSON file
with open('modified.geojson', 'w') as f:
    json.dump(geojson_data, f)