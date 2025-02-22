# tests/test_training.py
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_generate_training_plan():
    # Provide valid input data
    payload = {
        "bmi": 22.0,
        "daily_exercise": 30,
        "diet_quality": 7
    }
    response = client.post("/training/generate-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Check that a user_id exists and plan contains 10 steps
    assert "user_id" in data
    assert "plan" in data
    assert len(data["plan"]) == 10
    # Optionally, check that each step contains required fields
    for step in data["plan"]:
        assert "step_number" in step
        assert "description" in step
        assert "target_difficulty" in step
        assert "recommended_duration" in step
        assert "simulated_insight" in step

# You can add more tests for GET /training/plan/{user_id} and authentication endpoints.
