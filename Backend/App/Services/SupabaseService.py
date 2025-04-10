from supabase import create_client, Client
import os
from dotenv import load_dotenv
from App.Helpers.PasswordAuth import password_auth


# create a class to interact with Supabase
# it get the Supabase URL and the Supabase Anon Key from the settings
class SupabaseService:
    
    def __init__(self):

        
        current_file_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file_path))  # Adjust based on your file location
        print(f"Project root: {project_root}")
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


    def get_user(self, username):
        """Get user details from database based on username"""
        result = self.supabase.table("users").select("*").eq("username", username).limit(1).execute()
        
        if not result.data or not result.data[0]["active"]:
            return False

        return result
    def create_user(self, username, encrypted_password):
        """Create a new user in the database."""
        try:
            # Check if user already exists
            existing_user = self.get_user(username)
            if existing_user:
                return False
             
            # Insert new user
            result = self.supabase.table("users").insert({
                "username": username,
                "password": encrypted_password,
            }).execute()
            
            if not result.data:
                return False
                
            return result
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False



supabase_service = SupabaseService()