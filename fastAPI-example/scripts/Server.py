import os
import bcrypt
from fastapi import FastAPI, Form, Depends, HTTPException  
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
import jwt
from starlette.requests import Request
from supabase import create_client
from dotenv import load_dotenv
import datetime

def create_jwt_token(data: dict):
    """Generate JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})  # Add expiration time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# JWT Secret Key (replace this with a strong secret in production!)
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBbmRyZWEiLCJleHAiOjE3NDA2NzM1MDV9._ZiK2ypEM4j9_wZ1msHuLJuEFrpSfw9E3luOG5OvrpU"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 30  # Token validity duration

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:

        print(f"🔍 Received token: {token}")  # ✅ Debugging to see if FastAPI gets the token

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


app = FastAPI()
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/Login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Fetch user from Supabase
    response = supabase.table("users").select("password").eq("username", username).execute()

    if not response.data:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_password = response.data[0]["password"].encode("utf-8")

    # Verify password
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        token = create_jwt_token({"sub": username})
        return JSONResponse(content={"access_token": token, "token_type": "bearer"})

    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/fire_risk_map", response_class=JSONResponse)
async def dashboard(username: str = Depends(verify_jwt_token)):
    return {"message": f"Welcome, {username}! You have access to the Fire Risk Map."}

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    print(f"📌 Received request - Username: {username}")

    # Hash password before storing
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        # Insert user into Supabase
        response = supabase.table("users").insert({"username": username, "password": hashed_password}).execute()

        # Debugging: Print the full response
        print(f"Supabase Response: {response}")

        # Check for errors
        if response.data is None and response.error:
            if "duplicate key value" in str(response.error):  # Handle duplicate username error
                return {"error": "Username already exists"}
            return {"error": response.error["message"]}

        return {"message": "User registered successfully"}

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"error": "Internal Server Error"}



