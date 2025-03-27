from supabase import create_client
import hashlib
import secrets

from dotenv import load_dotenv
import os
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


# Hashes a given secret string using SHA-256 algorithm.
# Which is the algorithm of choice for this entire project
def hash_secret(secret: str):
    return hashlib.sha256(secret.encode()).hexdigest()


# Create a unique client_id for a business
# 1st part the 4 first letters in the business name (X's if its less than 4)
# 2nd part a random character from the name
# 3rd part 4 random hex values
def generate_client_id(business_name: str):
    prefix = ''.join(c for c in business_name if c.isalnum()).upper()
    prefix = (prefix + 'XXXX')[:4]
    rand_char = secrets.choice(business_name)
    rand_hex = secrets.token_hex(4)
    return f"{prefix}-{rand_char}-{rand_hex}"


# Create an API_CLIENT_SECRET (and save it)
# Note that the key is returned as a hash
# Therefore recommended to note the secret before loosing it. 
# As of now its saved to ./supabase_api_auth_example/.env for further use
def generate_client_secret():
    client_secret = secrets.token_urlsafe(32)
    with open("./supabase_api_auth_example/.env", "a") as env_file:
        env_file.write(f"API_CLIENT_SECRET={client_secret}\n")

    return hash_secret(client_secret), client_secret


def create_api_client(database, business_name: str):
    
    client_id = generate_client_id(business_name)
    
    client_secret_hash, client_secret = generate_client_secret()

    try:
        result = database.table('api_clients').insert({
            "client_id": client_id,
            "client_secret": client_secret_hash,
            "business_name": business_name,
            "active": True
        }).execute()

    except Exception as e:
        print(f"Error creating client: {str(e)}")
        raise Exception(f"Failed to create API client: {str(e)}")

    return {
        "client_id": client_id,
        "client_secret": client_secret,  # Return unhashed for initial setup
        "business_name": business_name
    }


if __name__ == "__main__":
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    business = "FirstClient"

    new_client = create_api_client(supabase, business)
    print(f"Created api_client information for business {new_client['business_name']}:")
    print(f"client id: {new_client['client_id']}")
    print(f"client secret: {new_client['client_secret']}")




