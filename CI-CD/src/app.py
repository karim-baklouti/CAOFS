from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import os
from datetime import datetime

# Environment variables
APP_NAME = os.getenv("APP_NAME", "User Management API")
APP_VERSION = os.getenv("APP_VERSION", "3.0")
MAX_USERS = int(os.getenv("MAX_USERS", "100"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Configure logging
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title=APP_NAME)

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

@app.get("/")
def read_root():
    return {
        "message": APP_NAME,
        "version": APP_VERSION,
        "max_users": MAX_USERS,
        "debug_mode": DEBUG_MODE,
        "current_users": len(users)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    global user_id_counter
    if len(users) >= MAX_USERS:
        raise HTTPException(status_code=400, detail=f"Maximum users limit ({MAX_USERS}) reached")
    user_data = user.model_dump()
    user_data["id"] = user_id_counter
    users[user_id_counter] = user_data
    logger.info(f"Created user: {user_data}")
    user_id_counter += 1
    return user_data

@app.get("/users", response_model=List[UserResponse])
def get_users():
    return list(users.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data
    return user_data

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    return {"message": "User deleted successfully"}