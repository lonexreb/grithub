# tests/test_training1.py
import uuid
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_generate_training_plan_with_new_fields():
    payload = {
        "height": 170,
        "weight": 70,
        "age": 25,
        "fitness_level": "Beginner",
        "injury_history": "",
        "target_goal": "Build Muscle"
    }
    
    response = client.post("/training/generate-plan", json=payload)
    assert response.status_code == 200, f"Response status code: {response.status_code}, detail: {response.text}"
    data = response.json()
    assert "user_id" in data, "Missing user_id in response"
    assert "plan" in data, "Missing plan in response"
    assert isinstance(data["plan"], list), "Plan is not a list"
    assert len(data["plan"]) == 10, f"Expected 10 steps, got {len(data['plan'])}"

if __name__ == "__main__":
    test_generate_training_plan_with_new_fields()
    print("Test passed!")
