from supabase import create_client
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Create a unique client_id for a business
def generate_client_id(business_name: str):
    prefix = ''.join(c for c in business_name if c.isalnum()).upper()
    prefix = (prefix + 'XXXX')[:4]
    rand_char = secrets.choice(business_name)
    rand_hex = secrets.token_hex(4)
    return f"{prefix}-{rand_char}-{rand_hex}"

# Generate a plaintext client_secret (no hashing for OAuth2)
def generate_client_secret():
    return secrets.token_urlsafe(32)

def create_api_client(database, business_name: str):
    client_id = generate_client_id(business_name)
    client_secret = generate_client_secret()

    try:
        result = database.table('api_clients').insert({
            "client_id": client_id,
            "client_secret": client_secret,  # Store plaintext
            "business_name": business_name,
            "active": True
        }).execute()

    except Exception as e:
        print(f"Error creating client: {str(e)}")
        raise Exception(f"Failed to create API client: {str(e)}")

    return {
        "client_id": client_id,
        "client_secret": client_secret,  # Return plaintext for initial setup
        "business_name": business_name
    }

if __name__ == "__main__":
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    business = "FirstClient"

    new_client = create_api_client(supabase, business)
    print(f"Created api_client information for business {new_client['business_name']}:")
    print(f"Client ID: {new_client['client_id']}")
    print(f"Client Secret: {new_client['client_secret']}")