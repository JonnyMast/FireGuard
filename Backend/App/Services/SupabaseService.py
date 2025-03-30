from supabase import create_client, Client
import os
from dotenv import load_dotenv


# create a class to interact with Supabase
# it get the Supabase URL and the Supabase Anon Key from the settings
class SupabaseService:
    
    def __init__(self):
        load_dotenv()
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

        self.supabase: Client = create_client(
            SUPABASE_URL,
            SUPABASE_ANON_KEY
        )


    def get_all_clients(self):
        response = self.supabase.table('api_clients').select('*').execute()
        return response.data
    
    
    def verify_client(self, client_id, client_secret):
        """Verify client credentials against database"""
        result = self.supabase.table("api_clients").select("client_secret", "active").eq("client_id", client_id).execute()
        return (result.data and 
                result.data[0]["client_secret"] == client_secret and
                result.data[0]["active"])
                
    def verify_user(self, username):
        """Verify if user exists and is active"""
        result = self.supabase.table("users").select("active").eq("username", username).execute()
        return result.data and result.data[0]["active"]


supabase_service = SupabaseService()