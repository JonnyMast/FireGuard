from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from App.Controllers.AuthController import auth_controller

router = APIRouter(prefix="/gen", tags=["authentication"])
security = HTTPBasic()

class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str

class UserCredentials(BaseModel):
    username: str
    password: str

# Client token endpoint
@router.post("/jwt/client")
async def generate_client_token(credentials: ClientCredentials):
    # Call controller to handle business logic
    token = auth_controller.GenerateClientToken(credentials.client_id, credentials.client_secret)
    return {"token": token, "token_type": "bearer"}


@router.post("/jwt/user")
async def generate_user_token(credentials: UserCredentials):
    # Call controller to handle business logic
    token = auth_controller.GenerateUserToken(credentials.username, credentials.password)
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    return {"token": token, "token_type": "bearer"}