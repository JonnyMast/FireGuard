from supabase import create_client, Client
from fireguard2.core.config import settings
from fireguard2.core.logger import setup_logger
logger = setup_logger(__name__)

if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
    raise ValueError("Supabase URL or API Key is missing in environment variables.")

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
logger.info(f"Connected to Supabase at: {settings.SUPABASE_URL}")



def get_user_by_username(username: str) -> dict | None:
    try:
        response = supabase.table("users").select("username, password").ilike("username", username).execute()
        user_data = response.data

        if user_data:
            logger.info(f"User found: {username}")
            return user_data[0]
        else:
            logger.info(f"No user found with username: {username}")
            return None

    except Exception as e:
        logger.warning(f"Unexpected error fetching user '{username}': {e}")
        return None


def insert_new_user(username: str, hashed_password: str) -> dict:
    try:
        response = supabase.table("users").insert({"username": username, "password": hashed_password}).execute()

        if response.data:
            logger.info(f"New user inserted: {username}")
            return {"message": "User inserted"}

        elif response.error:
            if "duplicate" in str(response.error).lower():
                logger.warning(f"Attempt to register existing username: {username}")
                return {"error": "Username already exists"}

            logger.error(f"Supabase returned error for user '{username}': {response.error}")
            return {"error": str(response.error)}

        logger.error(f"Unknown error during user insert: {username}")
        return {"error": "Unknown insert failure"}

    except Exception as e:
        logger.error(f"Exception inserting user '{username}': {e}")
        return {"error": "Internal Server Error"}
