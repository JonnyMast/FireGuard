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


supabase_service = SupabaseService()