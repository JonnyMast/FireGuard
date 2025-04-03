import os
import sys
import logging
import folium
import matplotlib.colors as mcolors
from dotenv import load_dotenv
from folium import Element
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location, FireRiskPrediction
from fireguard2.services import prediction_helper as ph

from fireguard2.core.logger import setup_logger
logger = setup_logger(__name__)

load_dotenv()

class MapHelper:

    @staticmethod
    def MakeMap(number_of_days: int = 10) -> None:
        """
        Generate a fire risk map and save it as static/fire_risk_map.html
        """

        # Validate API credentials
        api_key = os.getenv("MET_CLIENT_ID")
        if not api_key:
            logger.error("MET_CLIENT_ID not set in .env")
            return

        frc = METFireRiskAPI()
        obs_delta = ph.timedelta_days(number_of_days)

        kommunesentre = {
            "Bergen": Location(latitude=60.39299, longitude=5.32415),
            "Oslo": Location(latitude=59.9139, longitude=10.7522),
            "Trondheim": Location(latitude=63.4305, longitude=10.3951),
            "Førde": Location(latitude=61.4521, longitude=5.8535),
            #"Stongfjorden": Location(latitude=61.4561, longitude=5.0297),
        }

        cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["red", "yellow", "green"])
        fire_map = folium.Map(location=(61.0, 6.0), zoom_start=7)

        # Add logout button and JS
        extras = """
        <link rel="stylesheet" href="static/fire_risk_map_style.css">
        <div id="logoutContainer" class="leaflet-control leaflet-bar">
            <button id="logoutButton" class="leaflet-control-button">Log Out</button>
        </div>
        <script src="static/logout.js"></script>
        """
        fire_map.get_root().html.add_child(Element(extras))

        # Loop over each kommune
        for kommune, location in kommunesentre.items():
            logger.info(f"Fetching fire risk for {kommune}...")

            try:
                prediction: FireRiskPrediction = frc.compute_now(location, obs_delta)
                ttf = ph.calculate_minimum_ttf(prediction)
                norm_val = ph.normalize_max_fire_risk_value(ttf)
                color = mcolors.to_hex(cmap(norm_val))

                folium.CircleMarker(
                    location=(location.latitude, location.longitude),
                    radius=7,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    popup=f"{kommune}: {ttf:.2f}",
                ).add_to(fire_map)

            except Exception as e:
                logger.warning(f"Failed to fetch for {kommune}: {e}")

        # Save map to static folder
        static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
        os.makedirs(static_dir, exist_ok=True)
        output_path = os.path.join(static_dir, "fire_risk_map.html")

        try:
            fire_map.save(output_path)
            logger.info(f"Map saved to {output_path}")
        except Exception as e:
            logger.error(f"Could not save map: {e}")
