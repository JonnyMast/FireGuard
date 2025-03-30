from fastapi import APIRouter, HTTPException
from App.Services.SupabaseService import supabase_service
from pydantic import BaseModel

# Define a router for the henriktest table
router = APIRouter(prefix="/clients", tags=["client"])


# Define a Pydantic model for creating a new text in the henriktest table
class ClientCreate(BaseModel):
    text: str


# Get route to get all texts from the henriktest table
@router.get("/")
async def get_clients():
    try:
        clients = supabase_service.get_all_clients()
        return {"clients": clients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

