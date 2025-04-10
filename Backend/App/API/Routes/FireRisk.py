from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from App.Controllers.FireRiskController import risk_controller
from App.Helpers.JwtUtils import VerifyJwt
from App.Services.SupabaseService import supabase_service  # Adjust import based on your project structure

router = APIRouter(prefix="/fireguard", tags=["firerisk"])
security = HTTPBearer()

class LocationModel(BaseModel):
    city: str
    days: int

class CoordinateModel(BaseModel):
    latitude: float
    longitude: float
    days: int

# JWT verification dependency
async def verify_token(credentials: HTTPBearer = Security(security)):
    token = credentials.credentials
    if not VerifyJwt(token, supabase_service):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

@router.get("/firerisk/city")
async def get_prediction_from_name(city: str, days: int, authenticated: bool = Depends(verify_token)):
    # Call controller to handle business logic
    firerisk = risk_controller.PredictOnCityName(city, days)
    
    return firerisk

@router.get("/firerisk/coordinates")
async def get_prediction_from_coordinate(latitude: float, longitude: float, days: int, authenticated: bool = Depends(verify_token)):
    # Implement prediction logic here
    return False
