from App.Helpers.JwtUtils import CreateClientJwt, CreateUserJwt
from App.Services.SupabaseService import supabase_service
from fastapi import HTTPException

class AuthController:

    def GenerateClientToken(self, client_id: str, client_secret: str) -> str:
        """Business logic for client token generation"""
        if not supabase_service.verify_client(client_id, client_secret):
            raise HTTPException(status_code=401, detail="Invalid client credentials")
        
        return CreateClientJwt(client_id, client_secret)
    

    def GenerateUserToken(self, username: str, password: str) -> str:
        """Business logic for user token generation"""
        #Password handling imported from Helpers
        password_handled = False
        if password_handled:
            return CreateUserJwt()
        
        return None
        


auth_controller = AuthController()