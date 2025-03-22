from fastapi import FastAPI, HTTPException, Form, Header
from supabase import create_client
import jwt
from datetime import datetime, timedelta
import hashlib
import secrets

from dotenv import load_dotenv
import os
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

app = FastAPI()
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
SECRET_KEY = os.getenv("API_CLIENT_SECRET")
def hash_secret(secret: str):
    return hashlib.sha256(secret.encode()).hexdigest()

def generate_access_token(client_id: str):
    payload = {
        "sub": client_id,
        "exp": datetime.now() + timedelta(hours=1),  # 1-hour expiry
        "scope": "flashover-api"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_access_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["sub"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Token endpoint
@app.post("/oauth/token")
async def issue_token(
    client_id: str = Form(...),
    client_secret: str = Form(...),
    grant_type: str = Form(...)
):
    if grant_type != "client_credentials":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")
    
    response = supabase.table("api_clients")\
        .select("client_id, client_secret")\
        .eq("client_id", client_id)\
        .eq("active", True)\
        .execute()
    
    if not response.data or hash_secret(client_secret) != response.data[0]["client_secret"]:
        raise HTTPException(status_code=401, detail="Invalid client credentials")
    
    access_token = generate_access_token(client_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600
    }

# API endpoint
@app.get("/api")
async def get_flashover(lat: float, lon: float, authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    client_id = verify_access_token(token)
    # Your flashover logic here
    return {"time_to_flashover": 42}
    