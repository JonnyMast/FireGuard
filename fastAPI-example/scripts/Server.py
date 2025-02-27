import os
import bcrypt
from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/Login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Fetch user from Supabase
    response = supabase.table("users").select("password").eq("username", username).execute()
    
    if not response.data:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Incorrect username or password"})
    
    # Verify password
    stored_password = response.data[0]["password"].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return RedirectResponse(url="/fire_risk_map", status_code=303)

    return templates.TemplateResponse("login.html", {"request": request, "message": "Incorrect username or password"})

@app.get("/fire_risk_map", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("fire_risk_map.html", {"request": request})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    print(f"📌 Received request - Username: {username}")

    # Hash password before storing
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        # Insert user into Supabase
        response = supabase.table("users").insert({"username": username, "password": hashed_password}).execute()

        # Debugging: Print the full response
        print(f"📝 Supabase Response: {response}")

        # Check for errors
        if response.data is None and response.error:
            if "duplicate key value" in str(response.error):  # Handle duplicate username error
                return {"error": "Username already exists"}
            return {"error": response.error["message"]}

        return {"message": "User registered successfully"}

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"error": "Internal Server Error"}



