from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from App.Controllers.AuthController import auth_controller

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBasic()

class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str

class UserCredentials(BaseModel):
    username: str
    password: str

# Client token endpoint
@router.post("/jwt/verify")
async def get_client_token(credentials: ClientCredentials):
    # Call controller to handle business logic
    