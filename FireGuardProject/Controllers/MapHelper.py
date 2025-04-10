import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import datetime
import folium
import matplotlib.colors as mcolors
import numpy as np
from decouple import Config, RepositoryEnv
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location, FireRiskPrediction
from folium import Element
from folium.plugins import LocateControl
import Helpers.FireRiskPredictionHelper as FireRiskPredictionHelper

class MapHelper:
    @staticmethod
    def MakeMap(number_of_days: int = 10):
        """Generate fire risk map with proper environment handling."""
        try:
            # Configure logging once
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler("fire_risk_log.txt", encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            # Get project root directory (2 levels up from MapHelper.py)
            project_root = Path(__file__).parent.parent
            logging.info(f"Project root: {project_root}")

            # Load environment variables from project root
            env_path = project_root / '.env'
            logging.info(f"Looking for .env at: {env_path}")

            if not env_path.exists():
                logging.error(f"[ENV] File not found: {env_path}")
                raise FileNotFoundError(f"No .env file found at {env_path}")

            # Load environment variables
            load_dotenv(env_path)
            
            # Get API key
            api_key = os.getenv('MET_CLIENT_ID')
            if not api_key:
                logging.error("[ENV] MET_CLIENT_ID not found")
                raise ValueError("MET_CLIENT_ID not found in environment variables")

            logging.info(f"[ENV] MET_CLIENT_ID loaded successfully")

            # Initialize API client
            frc = METFireRiskAPI()

            kommunesentre = {
                "Bergen": Location(latitude=60.39299, longitude=5.32415),
                #"Stord": Location(latitude=59.77924, longitude=5.50075),
                #"Odda": Location(latitude=60.06928, longitude=6.54639),
                #"Voss": Location(latitude=60.62769, longitude=6.41594),
                "Førde": Location(latitude=61.45103, longitude=5.86358),
                #"Sogndal": Location(latitude=61.22934, longitude=7.10377),
                "Florø": Location(latitude=61.59939, longitude=5.03249),
                ##"Nordfjordeid": Location(latitude=61.90579, longitude=5.99109),
                "Tønsberg": Location(latitude=59.2671, longitude=10.4076),
                "Oslo": Location(latitude=59.9139, longitude=10.7522),
                "Trondheim": Location(latitude=63.4305, longitude=10.3951),
            }

            obs_delta = datetime.timedelta(days=number_of_days)

            # Center map in Hordaland, Sogn og Fjordane
            map_center = (61.0, 6.0)
            fire_map = folium.Map(location=map_center, zoom_start=7, zoom_control=False)
            LocateControl(
            auto_start=True,
            position='topleft',
            strings={'title': 'Show my location'},
            flyTo=True,
            
            icon='fa fa-map-marker',  # Font Awesome icon
            locateOptions={
                'maxZoom': 15,
                'enableHighAccuracy': True
            }
            ).add_to(fire_map)
        

            cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["red", "yellow", "green"])
            # In your MakeMap function, add this before saving the map:

            # Get project root and views directory paths
            project_root = Path(__file__).parent.parent
            views_dir = project_root / 'Views'

            # Update external files HTML with web-accessible paths and proper script loading
            external_files_html = """
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="/FireGuardProject/Views/FireRiskMapStyle.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
            </head>
            <body>
            <div class="controls-wrapper">
                <div id="daysControlContainer" class="leaflet-control leaflet-bar">
                    <input type="range" id="daysSlider" min="1" max="30" value="10" class="days-slider">
                    <span id="daysValue">10 days</span>
                    <button id="updateButton" class="update-button">Update Map</button>
                </div>
                <div id="logoutContainer" class="leaflet-control">   <button id="logoutButton" class="leaflet-control-button">Log Out</button>
                 </div>
                 
            </div>
                <script src="/FireGuardProject/Views/jwt_header.js"></script>
                <script src="/FireGuardProject/Views/Logout.js"></script>
                <script src="/FireGuardProject/Views/MapControls.js"></script>
            </body>
            """

            

            fire_map.get_root().html.add_child(Element(external_files_html))

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

            views_dir = os.path.join(project_root, 'Views')
            # Or more simply:
            output_path = os.path.join(views_dir, 'fire_risk_map.html')

            try:
                # Ensure Views directory exists
                os.makedirs(views_dir, exist_ok=True)

                # Save map
                fire_map.save(output_path)
                logging.info(f"[MAP] Saved to: {output_path}")
                logging.info("[MAP] Open in browser to view visualization")
            except Exception as e:
                logging.error(f"[ERROR] Could not save map: {str(e)}")
                logging.error("[INFO] Try saving to a different location")
                raise

            # Log fire risk overview
            logging.info("\n[FIRE RISK OVERVIEW]")
            #for kommune, risk_value in fire_risk_results.items():
                #logging.info(f"{kommune}: {risk_value:.2f}")

            return output_path
        except Exception as e:
            logging.error(f"[ERROR] {str(e)}")
            raise