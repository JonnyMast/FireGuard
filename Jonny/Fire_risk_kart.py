import sys
import os
import datetime
import folium
import matplotlib.colors as mcolors
import numpy as np
import logging
from decouple import Config, RepositoryEnv

# Konfigurer logging for både terminal og fil
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fire_risk_log.txt"),  # Logger til fil
        logging.StreamHandler(sys.stdout)  # Logger til terminal
    ]
)

# Legg til 'frcm'-mappen i sys.path slik at Python finner modulen
frcm_path = os.path.abspath("/Users/jonnyhugoy/Documents/frcm")
if frcm_path not in sys.path:
    sys.path.append(frcm_path)

from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

# Hent miljøvariabler fra .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
config = Config(RepositoryEnv(env_path))

# Sjekk om API-nøkkel er tilgjengelig
api_key = config('MET_CLIENT_ID', default='NOT FOUND')
logging.info(f"MET_CLIENT_ID: {api_key}")
if api_key == 'NOT FOUND':
    logging.error("ERROR: API key not found. Please check your .env file.")
    sys.exit(1)

# Opprett API-klienten
frc = METFireRiskAPI()

# Definer kommunesentrene i Hordaland og Sogn og Fjordane
kommunesentre = {
    "Bergen": Location(latitude=60.39299, longitude=5.32415),
    "Stord": Location(latitude=59.77924, longitude=5.50075),
    "Odda": Location(latitude=60.06928, longitude=6.54639),
    "Voss": Location(latitude=60.62769, longitude=6.41594),
    "Førde": Location(latitude=61.45103, longitude=5.86358),
    "Sogndal": Location(latitude=61.22934, longitude=7.10377),
    "Florø": Location(latitude=61.59939, longitude=5.03249),
    "Nordfjordeid": Location(latitude=61.90579, longitude=5.99109)
}

# Definer tidsperiode for observasjoner
obs_delta = datetime.timedelta(days=2)

# Opprett kart sentrert i Hordaland og Sogn og Fjordane
map_center = (61.0, 6.0)
fire_map = folium.Map(location=map_center, zoom_start=7)

# Fargekart fra grønn (lav risiko) til rød (høy risiko)
cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["green", "yellow", "red"])

# Generer simulerte verdier hvis API-feil oppstår
np.random.seed(42)

# Dictionary for å lagre alle brannrisikoverdier
fire_risk_results = {}

# Beregn og visualiser brannrisiko for hver kommune
for kommune, location in kommunesentre.items():
    logging.debug(f"Fetching fire risk for {kommune}...")
    fire_risk = frc.compute_now(location, obs_delta)
    
    # Debugging for å sjekke hva API-et returnerer
    logging.debug(f"Raw API response for {kommune}: {fire_risk}")
    
    # Hvis API-data er ugyldige, bruk simulert verdi
    if fire_risk is None or not isinstance(fire_risk, (float, int)) or not (0 <= fire_risk <= 1):
        fire_risk = np.random.uniform(0, 1)
        logging.warning(f"SIMULATED Fire Risk for {kommune}: {fire_risk:.2f}")
    else:
        logging.info(f"Fire Risk for {kommune}: {fire_risk:.2f}")
    
    # Lagre brannrisiko
    fire_risk_results[kommune] = fire_risk
    
    # Farge basert på brannrisiko
    color = mcolors.to_hex(cmap(fire_risk))  
    folium.CircleMarker(
        location=(location.latitude, location.longitude),
        radius=10 + fire_risk * 10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{kommune}: {fire_risk:.2f}",
    ).add_to(fire_map)

# Sti til lagringsplass
output_path = "fire_risk_map.html"

# Prøv å lagre kartet
try:
    fire_map.save(output_path)
    logging.info(f"- Brannrisikokart lagret til: {output_path}")
    logging.info("- Åpne filen i en nettleser for å se visualiseringen.")
except Exception as e:
    logging.error(f"⚠- Kunne ikke lagre kartet: {e}")
    logging.error("- Prøv å lagre filen i en annen mappe, f.eks. Skrivebordet.")

# Skriv ut en samlet oversikt over brannrisiko
logging.info("\n- Fire Risk Overview -")
for kommune, risk in fire_risk_results.items():
    logging.info(f"{kommune}: {risk:.2f}")
