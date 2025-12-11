from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "version" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_user():
    user_data = {"name": "Test User", "email": "test@example.com", "age": 30}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user():
    # First create a user
    user_data = {"name": "Get User", "email": "get@example.com", "age": 25}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Then get the user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_update_user():
    # First create a user
    user_data = {"name": "Update User", "email": "update@example.com", "age": 40}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    updated_data = {"name": "Updated User", "email": "updated@example.com", "age": 41}
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["age"] == 41

def test_delete_user():
    # First create a user
    user_data = {"name": "Delete User", "email": "delete@example.com", "age": 50}
    create_response = client.post("/users", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_user_not_found():
    response = client.get("/users/99999")
    assert response.status_code == 404
