from fastapi import APIRouter
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from App.Controllers.AuthController import auth_controller

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBasic()

class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str


# Client token endpoint
@router.post("/jwt/client")
async def get_client_token(credentials: ClientCredentials):
    # Call controller to handle business logic
    token = auth_controller.GenerateClientToken(credentials.client_id, credentials.client_secret)
    return {"access_token": token, "token_type": "bearer"}