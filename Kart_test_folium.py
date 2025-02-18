import folium
import pandas as pd
from folium.plugins import HeatMap

# Simulert brannrisikodata (erstatt dette med dine faktiske data)
fire_risk_data = [
    {"latitude": 60.383, "longitude": 5.3327, "TTF": 6.0},
    {"latitude": 60.387, "longitude": 5.3350, "TTF": 5.8},
    {"latitude": 60.390, "longitude": 5.3380, "TTF": 5.2},
    {"latitude": 60.395, "longitude": 5.3400, "TTF": 4.7},
    {"latitude": 60.400, "longitude": 5.3450, "TTF": 4.2}
]

# Opprett et Folium-kart sentrert på Bergen
m = folium.Map(location=[60.383, 5.3327], zoom_start=12)

# Funksjon for å bestemme farge basert på brannrisiko
def get_color(ttf):
    if ttf > 5.5:
        return "green"
    elif 4.5 <= ttf <= 5.5:
        return "orange"
    else:
        return "red"

# Legg til markører for hvert datapunkt
for data in fire_risk_data:
    folium.CircleMarker(
        location=[data["latitude"], data["longitude"]],
        radius=10,
        color=get_color(data["TTF"]),
        fill=True,
        fill_color=get_color(data["TTF"]),
        fill_opacity=0.6,
        popup=f"Brannrisiko (TTF): {data['TTF']}"
    ).add_to(m)

# Vis kartet
m.save("fire_risk_map.html")
m
import webbrowser

import webbrowser
import os

# Sjekk om filen eksisterer og åpne den
file_path = os.path.abspath("fire_risk_map.html")

if os.path.exists(file_path):
    webbrowser.open("file://" + file_path)
else:
    print("Filen ble ikke funnet:", file_path)
