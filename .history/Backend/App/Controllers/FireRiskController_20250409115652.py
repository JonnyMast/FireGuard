from App.Helpers.JwtUtils import CreateClientJwt, CreateUserJwt
from App.Helpers.PasswordAuth import password_auth
from App.Helpers import PredictionHelper as ph
from App.Helpers.LocationHelper import location_helper
from App.Services.SupabaseService import supabase_service
from fastapi import HTTPException
from frcm.frcapi import METFireRiskAPI
import os
from dotenv import load_dotenv
MET_CLIENT_ID = load_dotenv('MET_CLIENT_ID')
MET_CLIENT_SECRET = load_dotenv('MET_CLIENT_SECRET')


class FireRiskController:
    
    def PredictOnCityName(self, city: str, days):
        try:
            frc = METFireRiskAPI()
            location = location_helper.city_to_coordinates(city)
            obs_delta = ph.timedelta_days(days)
            print(obs_delta)
            prediction = frc.compute_now(location, obs_delta)
            return prediction
        except Exception as e :
            print(e)
            return False
    

    def PredictOnCoordinates(self, latitude: float, longitude: float, days):
        
        return False
        


risk_controller = FireRiskController()