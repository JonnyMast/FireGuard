from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fireguard2.core.security import create_jwt_token
from fireguard2.db.supabase import get_user_by_username, insert_new_user
from fireguard2.core.config import templates
from fireguard2.core.logger import setup_logger
import bcrypt

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Authenticate user and return JWT token."""
    logger.info(f"[LOGIN] Attempt from user: {username}")
    user = get_user_by_username(username)

    if not user:
        logger.warning(f"[LOGIN] Failed — user not found: {username}")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    stored_password = user["password"].encode("utf-8")

    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        token = create_jwt_token({"sub": username})
        token = token.decode("utf-8") if isinstance(token, bytes) else token
        logger.info(f"[LOGIN] Success for user: {username}")
        return JSONResponse(content={"access_token": token, "token_type": "bearer"})

    logger.warning(f"[LOGIN] Failed — wrong password for user: {username}")
    raise HTTPException(status_code=401, detail="Invalid username or password")

@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    """Register a new user with hashed password."""
    logger.info(f"[REGISTER] Attempt for user: {username}")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        result = insert_new_user(username, hashed_password)
        if result.get("error"):
            logger.warning(f"[REGISTER] Failed for user '{username}': {result['error']}")
            return JSONResponse(status_code=400, content={"error": result["error"]})
        
        logger.info(f"[REGISTER] Success for user: {username}")
        return {"message": "User registered successfully"}

    except Exception as e:
        logger.exception(f"[REGISTER] Internal error for user '{username}'")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serve the login page."""
    return templates.TemplateResponse("login.html", {"request": request})
