import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Import API routers
from fireguard2.api import auth, map

# Initialize FastAPI app
app = FastAPI(
    title="FireGuard API",
    version="1.0.0",
    description="RESTful API for FireGuard risk visualization system",
)

# -----------------------------
# CORS Middleware Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace with frontend URL(s) in production
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

# -----------------------------
# Static Files & Templates
# -----------------------------
base_dir = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static")

# -----------------------------
# Include Routers (Modular API)
# -----------------------------
app.include_router(auth.router, prefix="", tags=["Authentication"])
app.include_router(map.router, prefix="", tags=["Fire Risk Map"])
