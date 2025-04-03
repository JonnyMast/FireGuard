import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

class Settings:
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    TOKEN_EXPIRATION_MINUTES: int = 100

    # MET API
    MET_CLIENT_ID: str = os.getenv("MET_CLIENT_ID")
    MET_CLIENT_SECRET: str = os.getenv("MET_CLIENT_SECRET")


settings = Settings()

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)
