from supabase import create_client, Client
from app.core.config import settings

# create a class to interact with Supabase
# it get the Supabase URL and the Supabase Anon Key from the settings
class SupabaseService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )


    def get_all_from_henriktest(self):
        response = self.supabase.table('henriktest').select('*').execute()
        return response.data
    

    def get_all_users(self):
        response = self.supabase.table('users').select('*').execute()
        return response.data


    def get_user(self, user_id: int):
        response = self.supabase.table('users').select('*').execute().eq('id', user_id).execute()
        return response.data[0] if response.data else None


supabase_service = SupabaseService()