# tests/test_gamification.py
import uuid
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_add_xp_and_get_data():
    # Generate a unique user_id for testing
    user_id = str(uuid.uuid4())
    
    # Initially, the gamification data should be at 0 XP and level 1.
    response = client.get(f"/gamification/{user_id}")
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["xp"] == 0
    assert data["level"] == 1

    # Add 50 XP: Expect XP=50, level remains 1 (since 50 < 100)
    xp_to_add = 50
    response = client.post(f"/gamification/add-xp/{user_id}?xp={xp_to_add}")
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["xp"] == 50
    assert data["level"] == 1

    # Add another 60 XP: Total XP becomes 110, which should result in level 2.
    xp_to_add = 60
    response = client.post(f"/gamification/add-xp/{user_id}?xp={xp_to_add}")
    assert response.status_code == 200, response.json()
    data = response.json()
    assert data["xp"] == 110
    assert data["level"] == 2

if __name__ == "__main__":
    test_add_xp_and_get_data()
    print("Gamification tests passed.")
