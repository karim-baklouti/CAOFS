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
    return {"status": "healthy"}

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
