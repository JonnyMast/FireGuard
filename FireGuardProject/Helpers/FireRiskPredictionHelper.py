import sys
import os
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



def calculate_minimum_ttf(fire_risk_prediction: FireRiskPrediction) -> float:
    return min(risk.ttf for risk in fire_risk_prediction.firerisks)
     


def normalize_max_fire_risk_value(fire_risk_prediction: float) -> float:

    fire_risk_prediction = fire_risk_prediction- 4.0
    fire_risk_prediction = fire_risk_prediction / 2.5
    min_max_prediction:float = min(max(fire_risk_prediction,0) , 1)
    return min_max_prediction 
