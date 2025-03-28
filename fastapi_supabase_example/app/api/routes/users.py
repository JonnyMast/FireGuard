from fastapi import APIRouter, HTTPException
from app.services.supabase_service import supabase_service

# Define a router for the users table
router = APIRouter(prefix="/users", tags=["users"])

# Get route to get all users from the users table
@router.get("/")
async def get_users():
    try:
        users = supabase_service.get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Get route to get a specific user from the users table
# Note that the user_id is passed as a parameter in the route
@router.get("/{user_id}")
async def get_user(user_id: int):
    try:
        user = supabase_service.get_user(user_id)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))