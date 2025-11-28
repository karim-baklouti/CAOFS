from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Secure User Management API")

# Load secrets from environment
API_KEY = os.getenv("API_KEY", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
JWT_SECRET = os.getenv("JWT_SECRET", "")

users = {}
user_id_counter = 1

# Application state for readiness
app_ready = True

class User(BaseModel):
    name: str
    email: str
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/")
def read_root():
    return {
        "message": "Secure User Management API",
        "version": "5.0",
        "security": "API Key required"
    }

@app.get("/health")
def health_check():
    """
    Readiness probe endpoint.
    Returns 200 if the application is ready to serve traffic.
    Checks if required configurations are present.
    """
    if not app_ready:
        raise HTTPException(status_code=503, detail="Application not ready")
    
    # Check if critical configurations are available
    if not API_KEY:
        raise HTTPException(status_code=503, detail="API_KEY not configured")
    
    return {
        "status": "healthy",
        "ready": True,
        "checks": {
            "api_key": bool(API_KEY),
            "db_password": bool(DB_PASSWORD),
            "jwt_secret": bool(JWT_SECRET)
        }
    }

@app.get("/live")
def liveness_check():
    """
    Liveness probe endpoint.
    Returns 200 if the application process is alive.
    This is a simple check that doesn't validate dependencies.
    """
    return {
        "status": "alive",
        "service": "user-management-api"
    }

@app.get("/config-status")
def config_status(api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    return {
        "api_key_configured": bool(API_KEY),
        "db_password_configured": bool(DB_PASSWORD),
        "jwt_secret_configured": bool(JWT_SECRET)
    }

@app.post("/users", response_model=UserResponse)
def create_user(user: User, api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    global user_id_counter
    user_data = user.model_dump()
    user_data["id"] = user_id_counter
    users[user_id_counter] = user_data
    user_id_counter += 1
    return user_data

@app.get("/users", response_model=List[UserResponse])
def get_users(api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    return list(users.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User, api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data
    return user_data

@app.delete("/users/{user_id}")
def delete_user(user_id: int, api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": "User deleted successfully"}