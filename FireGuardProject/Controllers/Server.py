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
from FireGuard.FireGuardProject.Helpers.MapHelper import MakeMap
# Load environment variables
import logging
import asyncio
import sys


import sys
import os

print(sys.executable)
print(sys.path)

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
print(f"Added to path: {project_root}")

# Change this import:
# from FireGuardProject.Models.FireRiskPredictionHelper import maximum_fire_risk
# To this:
# Or more simply:
import Helpers.FireRiskPredictionHelper as FireRiskPredictionHelper


# Rest of imports remain the same
import datetime
import folium
import matplotlib.colors as mcolors
import numpy as np
import logging
from decouple import Config, RepositoryEnv
import datetime
import os
from dotenv import load_dotenv
from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location, FireRiskPrediction

load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# JWT Secret Key (replace this with a strong secret in production!)
SECRET_KEY = "7774614087add478b9dfacd0f621ed0b4108e45a9a9bbb36f63875ec2632c70985740496b1ccc623ee117a3dd684e6542244dda5c146cc727b0568cae05a037b"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 100  # Token validity duration

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def MakeMap(number_of_days: int = 10):
    number_of_days: int = 10
    print(os.getcwd())  # Shows where Python is currently running from
    
    load_dotenv()
    # This implementation avoids accedental uploads of keys, but require a .env file 
    # Make sure to add .env to .gitignore before pushing
    os.getenv('MET_CLIENT_ID')
    os.getenv('MET_CLIENT_SECRET')
    # Konfigurer logging for både terminal og fil
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("fire_risk_log.txt"),  # Logger til fil
            logging.StreamHandler(sys.stdout)  # Logger til terminal
        ]
    )



    # Hent miljøvariabler fra .env
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    config = Config(RepositoryEnv(env_path))

    # Sjekk om API-nøkkel er tilgjengelig
    api_key = config('MET_CLIENT_ID', default='NOT FOUND')
    logging.info(f"MET_CLIENT_ID: {api_key}")
    if api_key == 'NOT FOUND':
        logging.error("ERROR: API key not found. Please check your .env file.")
        sys.exit(1)

    frc = METFireRiskAPI()

    kommunesentre = {
        "Bergen": Location(latitude=60.39299, longitude=5.32415),
        "Stord": Location(latitude=59.77924, longitude=5.50075),
        "Odda": Location(latitude=60.06928, longitude=6.54639),
        "Voss": Location(latitude=60.62769, longitude=6.41594),
        "Førde": Location(latitude=61.45103, longitude=5.86358),
        "Sogndal": Location(latitude=61.22934, longitude=7.10377),
        "Florø": Location(latitude=61.59939, longitude=5.03249),
        "Nordfjordeid": Location(latitude=61.90579, longitude=5.99109),
        "Tønsberg": Location(latitude=59.2671, longitude=10.4076),
        "Oslo": Location(latitude=59.9139, longitude=10.7522),
        "Trondheim": Location(latitude=63.4305, longitude=10.3951),
    }

    obs_delta = datetime.timedelta(days=number_of_days)

    # Center map in Hordaland, Sogn og Fjordane
    map_center = (61.0, 6.0)
    fire_map = folium.Map(location=map_center, zoom_start=7)


    cmap = mcolors.LinearSegmentedColormap.from_list("fire_risk", ["red", "yellow", "green"])



    fire_risk_results = {}

    for kommune, location in kommunesentre.items():
        logging.debug(f"Fetching fire risk for {kommune}...")
        fire_risk: FireRiskPrediction = frc.compute_now(location, obs_delta)

        logging.debug(f"Raw API response for {kommune}: {fire_risk}")

        minimum_ttf = FireRiskPredictionHelper.calculate_minimum_ttf(fire_risk)
        

        fire_risk_results[kommune] = minimum_ttf
        
        normalized_max_fire_risk_value = FireRiskPredictionHelper.normalize_max_fire_risk_value(minimum_ttf)

        color = mcolors.to_hex(cmap(normalized_max_fire_risk_value))
        folium.CircleMarker(
            location=(location.latitude, location.longitude),
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=f"{kommune}: {minimum_ttf:.2f}",
        ).add_to(fire_map)

    output_path = r'FireGuard\FireGuardProject\Views\fire_risk_map.html'

    try:
        fire_map.save(output_path)
        logging.info(f"- Brannrisikokart lagret til: {output_path}")
        logging.info("- Åpne filen i en nettleser for å se visualiseringen.")
    except Exception as e:
        logging.error(f"⚠- Kunne ikke lagre kartet: {e}")
        logging.error("- Prøv å lagre filen i en annen mappe, f.eks. Skrivebordet.")
    logging.info("\n- Fire Risk Overview -")
    for kommune, risk_value in fire_risk_results.items():
        logging.info(f"{kommune}: {risk_value:.2f}")
    return 


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
        return RedirectResponse(url="/")  # Redirect to login page

    token = authorization.split(" ")[1]  # Extract token after "Bearer "
    print(f"🔍 Extracted Token: {token}")

    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        logging.info(f"✅ Serving fire_risk_map.html for user: {username}")

        MakeMap()
        print(f"✅ Serving fire_risk_map.html for user: {username}")
        return FileResponse("Views/fire_risk_map.html")

    except jwt.ExpiredSignatureError:
        print("❌ Token expired. Redirecting to login page.")
        return RedirectResponse(url="/")

    except jwt.InvalidTokenError:
        print("❌ Invalid token. Redirecting to login page.")
        return RedirectResponse(url="/")


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