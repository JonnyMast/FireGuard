from App.Helpers.JwtUtils import CreateClientJwt, CreateUserJwt
from App.Helpers.PasswordAuth import password_auth
from App.Services.SupabaseService import supabase_service
from fastapi import HTTPException


class AuthController:
    def GenerateClientToken(self, client_id: str, client_secret: str) -> str:
        """Business logic for client token generation"""
        if not supabase_service.verify_client(client_id, client_secret):
            raise HTTPException(status_code=401, detail="Invalid client credentials")

        return CreateClientJwt(client_id, client_secret)

    def GenerateUserToken(self, username: str, password: str) -> str:
        """Business logic for user token generation
        Get user from db
        Check password
        Create JWT
        """
        user = supabase_service.get_user(username)
        if not user:
            return None

        db_pass = user.data[0]["password"]

        pass_match = password_auth.CheckPass(password, db_pass)
        if not pass_match:
            return None

        return CreateUserJwt(username)


auth_controller = AuthController()
