from fastapi import APIRouter, HTTPException
from app.services.supabase_service import supabase_service
from pydantic import BaseModel

# Define a router for the henriktest table
router = APIRouter(prefix="/henriktest", tags=["henriktest"])


# Define a Pydantic model for creating a new text in the henriktest table
class HenrikTestCreate(BaseModel):
    text: str


# Get route to get all texts from the henriktest table
@router.get("/")
async def get_henriktests():
    try:
        texts = supabase_service.get_all_from_henriktest()
        return {"texts": texts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Post route to create a new text in the henriktest table
@router.post("/")
async def create_henriktest(henriktest: HenrikTestCreate):
    try:
        new_text = supabase_service.create_henriktest(henriktest.model_dump())
        return {"new_text": new_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

