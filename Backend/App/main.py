from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App.API.Routes import Generate, FireRisk

app = FastAPI(title="FastAPI Supabase Example")

# Configure CORS
origins = [
    "http://localhost:8080",    # VS Code Live Server
    "http://localhost:8000",    # Common React port
    "http://127.0.0.1:8080",    # VS Code Live Server alternative URL
    "http://127.0.0.1:8000",    # Your FastAPI server (for same-origin requests)
    # Add your production domain when deploying
    # "https://yourapp.com",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Specify allowed origins instead of "*" for security
    allow_credentials=True,     # Allow cookies (if needed)
    allow_methods=["*"],        # Allow all methods
    allow_headers=["*"],        # Allow all headers
)

# Define which routers to include 
# Note the prefixes "/api" for each router
# This means that the routes will be available at 127.0.0.1/api/{route}
app.include_router(Generate.router, prefix="/api")
app.include_router(FireRisk.router, prefix="/api")

# Define a root path
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Supabase!"}