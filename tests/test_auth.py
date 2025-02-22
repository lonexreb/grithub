# tests/test_auth.py
import uuid
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register_and_login():
    # Generate a unique email for each test run
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "strongpassword"
    }
    
    # Register the user
    reg_response = client.post("/auth/register", json=user_data)
    assert reg_response.status_code == 200, f"Registration failed: {reg_response.json()}"
    reg_data = reg_response.json()
    assert "id" in reg_data
    assert reg_data["email"] == user_data["email"]
    
    # Attempt login with the same credentials
    login_response = client.post("/auth/login", json=user_data)
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
