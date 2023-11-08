#!/usr/bin/env python3

import folium
import plotly.express as px
import plotly.graph_objects as go
import csv
import json
import math
import time
import pandas as pd
from geopy.geocoders import Nominatim

addresses = [
    "615 W Edison Rd, Mishawaka, IN 46545",
    "236 W Edison Rd Suite 1, Mishawaka, IN 46545",
    "6502 Grape Rd, Mishawaka, IN 46545",
    "620 W Edison Rd, Mishawaka, IN 46545",
    "317 W University Dr, Mishawaka, IN 46545",
    "235 S Michigan St, South Bend, IN 46601",
    "2206 E Mishawaka Ave, South Bend, IN 46615",
    "2920 W Western Ave, South Bend, IN 46619",
    "618 S Pulaski St, South Bend, IN 46619",
    "1639 N Ironwood Dr, South Bend, IN 46635",
    "213 N Main St, South Bend, IN 46601"
]


# Initialize the map
map_center = [0, 0]  # Initialize with latitude and longitude of your choice
mymap = folium.Map(location=map_center, zoom_start=2)

# Initialize a geolocator
geolocator = Nominatim(user_agent="mine")

# Iterate through the addresses, geocode them, and add markers to the map
for address in addresses:
    location = geolocator.geocode(address,timeout=None)
    time.sleep(2)
    print(address)
    if location:
        lat, lon = location.latitude, location.longitude
        folium.Marker([lat, lon], tooltip=address).add_to(mymap)

# Save the map to an HTML file or display it in a Jupyter Notebook
mymap.save("address_map.html")
