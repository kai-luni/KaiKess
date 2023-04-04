import csv
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Read school data from CSV file
school_data = []
with open('schools.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        school_data.append((row['school'], int(row['kess_index']), row['gps']))

# Find GPS coordinates for each school
geolocator = Nominatim(user_agent="school_locator")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

coordinates = []

for school, kess_index, gps in school_data:
    if gps:
        lat, lon = map(float, gps.split(','))
        coordinates.append((lat, lon, kess_index, school))
    else:
        location = geocode(f"{school} Hamburg Germany")
        if location:
            coordinates.append((location.latitude, location.longitude, kess_index, school))
        else:
            print(f"Couldn't find coordinates for {school}")

# Function to assign color based on KESS index
def kess_index_color(kess_index):
    colors = ['darkpurple', 'red', 'lightred', 'orange', 'lightgreen', 'darkgreen']
    return colors[kess_index - 1]

# Create a map with the school coordinates and KESS index
m = folium.Map(location=[53.5500, 10.0000], zoom_start=12)

for lat, lon, kess_index, school_loc in coordinates:
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{school_loc}</b><br>KESS index: {kess_index}",
        icon=folium.Icon(color=kess_index_color(kess_index)),
    ).add_to(m)

m.save('schools_map_colored.html')
