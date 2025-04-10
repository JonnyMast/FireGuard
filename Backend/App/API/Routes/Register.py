from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from App.Services.SupabaseService import supabase_service
from App.Helpers.PasswordAuth import password_auth

router = APIRouter()

class RegisterModel(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register_user(user_data: RegisterModel):
    """
    Register a new user.
    
    Args:
        user_data: User registration information
        
    Returns:
        Dict with success message
    """
    # Check if username already exists
    existing_user = supabase_service.get_user(user_data.username)
    if existing_user and existing_user.data:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    
    # Hash the password
    encrypted_password = password_auth.CryptPass(user_data.password)
    
    # Create new user in database
    try:
        result = supabase_service.create_user(user_data.username, encrypted_password)
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to create user"
            )
        
        return {"message": "User registered successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration error: {str(e)}"
        )