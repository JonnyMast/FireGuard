import os
from dotenv import load_dotenv

load_dotenv()

# This class will hold all the settings for the application
# It will read the Supabase URL and Supabase Anon Key from the .env file
class Settings:
    PROJECT_NAME: str = "FastAPI Supabase Example"
    VERSION: str = "0.1.0"
    
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY")

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise ValueError("Missing SUPABASE credentials in .env file, please add SUPABASE_URL and SUPABASE_ANON_KEY (DO NOT COMMIT .env FILE without .gitignore)")

settings = Settings()