from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from datetime import datetime

# Simple logging to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="User Management API")

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
    logger.info("Root endpoint accessed")
    return {"message": "FastAPI User Management", "version": "2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    global user_id_counter
    user_data = user.model_dump()
    user_data["id"] = user_id_counter
    users[user_id_counter] = user_data
    logger.info(f"Created user: {user_data}")
    user_id_counter += 1
    return user_data

@app.get("/users", response_model=List[UserResponse])
def get_users():
    logger.info(f"Retrieved {len(users)} users")
    return list(users.values())

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved user: {user_id}")
    return users[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump()
    user_data["id"] = user_id
    users[user_id] = user_data
    logger.info(f"Updated user: {user_data}")
    return user_data

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[user_id]
    logger.info(f"Deleted user: {user_id}")
    return {"message": "User deleted successfully"}