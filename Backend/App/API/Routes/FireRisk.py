from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from App.Controllers.FireRiskController import risk_controller

router = APIRouter(prefix="/fireguard", tags=["firerisk"])
security = HTTPBasic()

class LocationModel(BaseModel):
    city: str
    days: int

class CoordinateModel(BaseModel):
    latitude: float
    longitude: float
    days: int


@router.get("/firerisk/city")
async def get_prediction_from_name(location: LocationModel):
    # Call controller to handle business logic
    firerisk = risk_controller.PredictOnCityName(location.city, location.days)
    
    return firerisk


@router.get("/firerisk/coordinates")
async def get_prediction_from_coordinate(location: CoordinateModel):
    return False
