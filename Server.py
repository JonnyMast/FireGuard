from fastapi import FastAPI, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

# Hardcoded valid credentials (replace with a database in production)
VALID_CREDENTIALS = {
    "admin": "1234",
    "user": "password"
}

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 for rendering HTML templates
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/Login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "message": "Incorrect username or password"})

@app.get("/fire_risk_map", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

