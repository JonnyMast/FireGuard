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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Header

# Load environment variables
import logging
import asyncio
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
    print(f"Added to path: {project_root}")

from Controllers.MapHelper import MapHelper


# Now import using the correct path


load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# JWT Secret Key (replace this with a strong secret in production!)
SECRET_KEY = "7774614087add478b9dfacd0f621ed0b4108e45a9a9bbb36f63875ec2632c70985740496b1ccc623ee117a3dd684e6542244dda5c146cc727b0568cae05a037b"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 1000  # Token validity duration

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



def create_jwt_token(data: dict):
    """Generate JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})  # Add expiration time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    print(f"🔍 Received token in FastAPI: {token}")  # ✅ Debugging

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        print(f"✅ Token valid for user: {username}")  # ✅ Debugging
        return username

    except jwt.ExpiredSignatureError:
        print("❌ Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    
    except jwt.InvalidTokenError:
        print("❌ Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()

# Mount the current directory as a View directory
app.mount("/FireGuardProject/Views", StaticFiles(directory="Views"), name="Views")

templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("/Views/Login.html", {"request": request, "message": ""})

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

@app.get("/fire_risk_map", response_class=FileResponse)
async def fire_risk_page(request: Request, authorization: str = Header(None)):
    """ Authenticate user before serving the fire risk map page. """
    if authorization is None or not authorization.startswith("Bearer "):
        print("❌ No valid Authorization header found. Redirecting to login page.")
        print(authorization)
        return RedirectResponse(url="/")  # Redirect to login page

    token = authorization.split(" ")[1]  # Extract token after "Bearer "
    print(f"🔍 Extracted Token: {token}")


    # Decode JWT token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    logging.info(f"✅ Serving fire_risk_map.html for user: {username}")

    #MapHelper.MakeMap()
    print(f"✅ Serving fire_risk_map.html for user: {username}")
    return FileResponse("Views/fire_risk_map.html")



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