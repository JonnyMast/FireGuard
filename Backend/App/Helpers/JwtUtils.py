import jwt
import time
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
CLIENT_TOKEN_EXPIRY = 3600
USER_TOKEN_EXPIRY = 3600


# Client JWT Creation
def CreateClientJwt(client_id: str, client_secret: str) -> str:
    """
    Create a JWT for an API client.
    
    Args:
        client_id (str): The client's unique identifier
        client_secret (str): The client's secret (included in payload)
    
    Returns:
        str: A signed JWT for the client
    """
    payload = {
        "sub": client_id,
        "client_secret": client_secret,  # Included for client validation
        "iat": int(time.time()),
        "exp": int(time.time()) + CLIENT_TOKEN_EXPIRY,
        "type": "client"  # Optional: distinguish token type
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# User JWT Creation
def CreateUserJwt(username: str) -> str:
    """
    Create a JWT for a user.
    
    Args:
        username (str): The user's unique identifier
    
    Returns:
        str: A signed JWT for the user
    """
    payload = {
        "sub": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + USER_TOKEN_EXPIRY,
        "type": "user"  # Optional: distinguish token type
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# Shared Verification (with type-specific checks)
def VerifyJwt(token: str, supabase_service) -> bool:
    """
    Verify a JWT (client or user) and validate against the database.
    
    Args:
        token (str): The JWT to verify
        supabase_service: Instance of SupabaseService
    
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        token_type = decoded.get("type")
        sub = decoded["sub"]

        if token_type == "client":
            client_secret = decoded.get("client_secret")
            return supabase_service.VerifyClient(sub, client_secret)
        
        elif token_type == "user":
            return supabase_service.VerifyUser(sub)
        
        else:
            return False
        
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False