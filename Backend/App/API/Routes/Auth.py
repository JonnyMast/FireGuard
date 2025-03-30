from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from App.Helpers.JwtUtils import CreateClientJwt, CreateUserJwt
from App.Services.SupabaseService import supabase_service

router = APIRouter(prefix="/auth", tags=["authentication"])

security = HTTPBasic()

class ClientCredentials(BaseModel):
    client_id: str
    client_secret: str

# Client token endpoint
@router.post("/jwt/client")
async def get_client_token(credentials: ClientCredentials):
    """
    Get a JWT token for API client access
    """
    # Verify client credentials
    if not supabase_service.verify_client(credentials.client_id, credentials.client_secret):
        raise HTTPException(
            status_code=401, 
            detail="Invalid client credentials"
        )
    
    # Generate token
    token = CreateClientJwt(credentials.client_id, credentials.client_secret)
    return {"access_token": token, "token_type": "bearer"}

# User token endpoint (if needed)
class UserCredentials(BaseModel):
    username: str
    password: str

@router.post("/jwt/user")
async def get_user_token(credentials: UserCredentials):
    """
    Get a JWT token for user access
    """
    # Verify user credentials (add your password verification logic)
    # This is just a placeholder - implement proper password checking
    if not verify_user_password(credentials.username, credentials.password):
        raise HTTPException(
            status_code=401, 
            detail="Invalid username or password"
        )
    
    # Generate token
    token = CreateUserJwt(credentials.username)
    return {"access_token": token, "token_type": "bearer"}

def verify_user_password(username: str, password: str) -> bool:
    # Implement proper password verification against your database
    # This is just a placeholder
    return True