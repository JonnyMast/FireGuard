import requests
import datetime
from collections import namedtuple

# Definer API-klasse og feilhåndtering
class FireRiskAPI:
    def __init__(self, api_url, client_id, client_secret):
        self.api_url = api_url
        self.client_id = client_id
        self.client_secret = client_secret

    def get_fire_risk(self, location, forecast_delta):
        """Henter brannrisiko basert på lokasjon og tid."""
        params = {
            "lat": location.latitude,
            "lon": location.longitude,
            "forecast_delta": forecast_delta,
        }
        try:
            response = requests.get(self.api_url, params=params, auth=(self.client_id, self.client_secret))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"⚠️ Feil ved henting av brannrisiko: {e}")
            return None

# Definer lokasjonsklasse
Location = namedtuple("Location", ["latitude", "longitude"])

# 🔥 Kommuner i Vestland med koordinater
vestland_kommuner = {
    "Gloppen": (61.7760, 6.1895),
    "Bergen": (60.3913, 5.3221),
    "Førde": (61.4520, 5.8636),
    "Voss": (60.6210, 6.4222),
}

# API-konfigurasjon
API_URL = "https://fireguard.api/fire-risk"
CLIENT_ID = "din_client_id"
CLIENT_SECRET = "ditt_client_secret"

# Opprett API-klient
frc = FireRiskAPI(API_URL, CLIENT_ID, CLIENT_SECRET)

# Definer risikogrense og periode for observasjoner
RISIKO_GRENSE = 5.0
forecast_delta = datetime.timedelta(hours=24)

# Liste for kommuner med høy brannrisiko
fire_risk_results = []

# Hent brannrisiko for hver kommune
for kommune, (lat, lon) in vestland_kommuner.items():
    location = Location(latitude=lat, longitude=lon)
    try:
        fire_risk = frc.get_fire_risk(location, forecast_delta)

        # Debugging: Sjekk API-respons
        print(f"📡 API-respons for {kommune}: {fire_risk}")

        # Sjekk om `fire_risk` er gyldig
        if not fire_risk or "data" not in fire_risk:
            print(f"❌ Ingen gyldige data for {kommune}, hopper over...")
            continue

        # Hent TTF-verdier (brannrisiko) og vindhastigheter
        ttf_values = [entry["TTF"] for entry in fire_risk["data"] if "TTF" in entry]
        wind_speeds = [entry["WindSpeed"] for entry in fire_risk["data"] if "WindSpeed" in entry]

        if not ttf_values:
            print(f"❌ Ingen TTF-verdier funnet for {kommune}")
            continue

        max_ttf = max(ttf_values)
        avg_wind_speed = sum(wind_speeds) / len(wind_speeds) if wind_speeds else None

        # Legg til kommunen i listen hvis risikoen er høy
        if max_ttf >= RISIKO_GRENSE:
            fire_risk_results.append({
                "Kommune": kommune,
                "Maksimal TTF": max_ttf,
                "Gjennomsnittlig Vindhastighet": avg_wind_speed
            })

    except Exception as e:
        print(f"❌ Feil ved henting av brannrisiko for {kommune}: {e}")

# ✅ Utskrift av resultater
print("\n🔥 Kommuner med høy brannrisiko:")
for result in fire_risk_results:
    print(f"{result['Kommune']}: Maksimal TTF={result['Maksimal TTF']:.2f}, Vindhastighet={result['Gjennomsnittlig Vindhastighet']:.2f} m/s")
