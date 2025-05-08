import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, RedirectResponse
from fireguard2.core.security import verify_jwt_token
from fireguard2.services.map_helper import MapHelper
from fireguard2.core.logger import setup_logger
logger = setup_logger(__name__)


router = APIRouter()


@router.get("/fire_risk_map")
async def fire_risk_page(request: Request, username: str = Depends(verify_jwt_token)):
    """
    Authenticated route. Generates and returns the fire_risk_map.html file.
    """
    try:
        logger.info(f"Authenticated fire risk map request from: {username}")

        # Trigger map generation
        MapHelper.MakeMap()

        map_path = os.path.join(os.path.dirname(__file__), "..", "static", "fire_risk_map.html")
        return FileResponse(path=map_path, media_type="text/html")

    except Exception as e:
        print(f"Map generation or delivery failed: {e}")
        return RedirectResponse(url="/")  # Fallback to login
