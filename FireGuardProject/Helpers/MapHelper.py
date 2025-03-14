import sys
import os

print(sys.executable)
print(sys.path)

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
print(f"Added to path: {project_root}")

# Change this import:
# from FireGuardProject.Models.FireRiskPredictionHelper import maximum_fire_risk
# To this:
# Or more simply:
import Helpers.FireRiskPredictionHelper as FireRiskPredictionHelper


# Rest of imports remain the same
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


class MapHelper:




    def MakeMap(number_of_days: int = 10):
        number_of_days: int = 10
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

        frc = METFireRiskAPI()

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

        obs_delta = datetime.timedelta(days=number_of_days)

        # Center map in Hordaland, Sogn og Fjordane
        map_center = (61.0, 6.0)
        fire_map = folium.Map(location=map_center, zoom_start=7)


        cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["red", "yellow", "green"])



        fire_risk_results = {}

        for kommune, location in kommunesentre.items():
            logging.debug(f"Fetching fire risk for {kommune}...")
            fire_risk: FireRiskPrediction = frc.compute_now(location, obs_delta)

            logging.debug(f"Raw API response for {kommune}: {fire_risk}")

            minimum_ttf = FireRiskPredictionHelper.calculate_minimum_ttf(fire_risk)
            

            fire_risk_results[kommune] = minimum_ttf
            
            normalized_max_fire_risk_value = FireRiskPredictionHelper.normalize_max_fire_risk_value(minimum_ttf)

            color = mcolors.to_hex(cmap(normalized_max_fire_risk_value))
            folium.CircleMarker(
                location=(location.latitude, location.longitude),
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f"{kommune}: {minimum_ttf:.2f}",
            ).add_to(fire_map)

      # To this (using os.path.join for cross-platform compatibility):
        output_path = os.path.join('Views', 'fire_risk_map.html')

        # Or more simply:
        output_path = 'Views/fire_risk_map.html'  # Forward slashes work on both Windows and Linux
        try:
            fire_map.save(output_path)
            logging.info(f"- Brannrisikokart lagret til: {output_path}")
            logging.info("- Åpne filen i en nettleser for å se visualiseringen.")
        except Exception as e:
            logging.error(f"⚠- Kunne ikke lagre kartet: {e}")
            logging.error("- Prøv å lagre filen i en annen mappe, f.eks. Skrivebordet.")
        logging.info("\n- Fire Risk Overview -")
        for kommune, risk_value in fire_risk_results.items():
            logging.info(f"{kommune}: {risk_value:.2f}")
        return 