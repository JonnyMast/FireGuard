import sys
import os
import sys
print(sys.executable)
print(sys.path)


# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
print("Project root:", project_root)
sys.path.append(project_root)

# Print current working directory and Python path
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)


# Now update the import statement to use the correct path
from Models.FireRiskPredictionHelper import maximum_fire_risk
import datetime
import folium
import matplotlib.colors as mcolors
import numpy as np
import logging
from decouple import Config, RepositoryEnv
import datetime
import os
from dotenv import load_dotenv
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location, FireRiskPrediction




print(os.getcwd())  # Shows where Python is currently running from

load_dotenv()
# This implementation avoids accedental uploads of keys, but require a .env file 
# Make sure to add .env to .gitignore before pushing
os.getenv('MET_CLIENT_ID')
os.getenv('MET_CLIENT_SECRET')





# Konfigurer logging for både terminal og fil
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fire_risk_log.txt"),  # Logger til fil
        logging.StreamHandler(sys.stdout)  # Logger til terminal
    ]
)



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
    "Nordfjordeid": Location(latitude=61.90579, longitude=5.99109),
    "Tønsberg": Location(latitude=59.2671, longitude=10.4076),
    "Oslo": Location(latitude=59.9139, longitude=10.7522),
    "Trondheim": Location(latitude=63.4305, longitude=10.3951),
}

# Definer tidsperiode for observasjoner
obs_delta = datetime.timedelta(days=2)

# Opprett kart sentrert i Hordaland og Sogn og Fjordane
map_center = (61.0, 6.0)
fire_map = folium.Map(location=map_center, zoom_start=7)

# Fargekart fra grønn (lav risiko) til rød (høy risiko)
cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["red", "yellow", "green"])



# Dictionary for å lagre alle brannrisikoverdier
fire_risk_results = {}

# Beregn og visualiser brannrisiko for hver kommune
for kommune, location in kommunesentre.items():
    logging.debug(f"Fetching fire risk for {kommune}...")
    fire_risk: FireRiskPrediction = frc.compute_now(location, obs_delta)

    # Debugging for å sjekke hva API-et returnerer
    logging.debug(f"Raw API response for {kommune}: {fire_risk}")
    # Lagre brannrisiko
    fire_risk_results[kommune] = fire_risk
    # Farge basert på brannrisiko
    maximum_fire_risk = FireRiskPredictionHelper.maximum_fire_risk(fire_risk)
    normalize_max_fire_risk_value = FireRiskPredictionHelper.normalize_max_fire_risk_value(maximum_fire_risk)

    
    color = mcolors.to_hex(cmap(normalize_max_fire_risk_value))
    folium.CircleMarker(
        location=(location.latitude, location.longitude),
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{kommune}: {maximum_fire_risk:.2f}",
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
    logging.info(f"{kommune}: {maximum_fire_risk:.2f}")
