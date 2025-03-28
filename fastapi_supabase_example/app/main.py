from fastapi import FastAPI
from app.api.routes import users, henriktest

app = FastAPI(title="FastAPI Supabase Example")

# Define which routers to include 
# Note the prefixes "/api" for each router
# This means that the routes will be available at 127.0.0.1/api/{route}
app.include_router(users.router, prefix="/api")
app.include_router(henriktest.router, prefix="/api")

# Define a root path
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Supabase!"}