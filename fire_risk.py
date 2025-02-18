import folium
import matplotlib.colors as mcolors
import numpy as np
import os

# Kommunesentrene med koordinater
kommunesentre = {
    "Bergen": (60.39299, 5.32415),
    "Stord": (59.77924, 5.50075),
    "Odda": (60.06928, 6.54639),
    "Voss": (60.62769, 6.41594),
    "Førde": (61.45103, 5.86358),
    "Sogndal": (61.22934, 7.10377),
    "Florø": (61.59939, 5.03249),
    "Nordfjordeid": (61.90579, 5.99109)
}

# Simulerte brannrisiko-verdier (0 = lav, 1 = høy) – erstatt med API-data
np.random.seed(42)
fire_risk_values = {kommune: np.random.uniform(0, 1) for kommune in kommunesentre}

# Fargekart fra grønn (lav risiko) til rød (høy risiko)
cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["green", "yellow", "red"])

# Opprett kart sentrert i Hordaland og Sogn og Fjordane
map_center = (61.0, 6.0)
fire_map = folium.Map(location=map_center, zoom_start=7)

# Legg til markører for hver kommune med farge basert på brannrisiko
for kommune, (lat, lon) in kommunesentre.items():
    risk = fire_risk_values[kommune]
    color = mcolors.to_hex(cmap(risk))  # Konverter fargekart-verdi til HEX
    folium.CircleMarker(
        location=(lat, lon),
        radius=10 + risk * 10,  # Større sirkel for høyere risiko
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{kommune}: {risk:.2f}",
    ).add_to(fire_map)

# Sti til lagringsplass
output_path = "/Users/jonnyhugoy/Documents/fire_risk_map.html"

# Prøv å lagre kartet
try:
    fire_map.save(output_path)
    print(f"✅ Brannrisikokart lagret til: {output_path}")
    print("📂 Åpne filen i en nettleser for å se visualiseringen.")
except Exception as e:
    print(f"⚠️ Kunne ikke lagre kartet: {e}")
    print("❗ Prøv å lagre filen i en annen mappe, f.eks. Skrivebordet.")

