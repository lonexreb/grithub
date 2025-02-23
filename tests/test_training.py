# tests/test_training.py
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# A stable mock 10-card plan matching your training_plan structure:
MOCK_RESPONSE = {
    "trainingPlanName": "Mock Training Plan",
    "cards": [
        {
            "cardNumber": i,
            "title": f"Phase {i}",
            "objectives": [f"Objective {i}"],
            "routine": [
                # Example routine item with optional fields
                {
                    "exercise": "Exercise A",
                    "sets": 3,
                    "reps": 12,
                    "rest": "60 sec",
                    "description": f"Routine item for card {i}"
                }
            ],
            "challenges": [f"Challenge {i}-1", f"Challenge {i}-2"]
        }
        for i in range(1, 11)
    ]
}

@pytest.mark.order(1)
@patch("services.training_service.generate_plan_using_openai")  
def test_generate_training_plan_valid_input(mock_ai):
    """
    1) Mocks the AI service to return a stable 10-card plan.
    2) POST /training/generate-plan with a valid payload.
    3) Expects top-level keys: user_id, trainingPlanName, cards (length 10).
    """
    mock_ai.return_value = MOCK_RESPONSE

    payload = {
        "height": 170.0,
        "weight": 70.0,
        "age": 25,
        "fitness_level": "Beginner",
        "injury_history": "",
        "target_goal": "Increase stamina"
    }
    response = client.post("/training/generate-plan", json=payload)
    assert response.status_code == 200, f"Status code: {response.status_code}, detail: {response.text}"

    data = response.json()
    assert "user_id" in data, "Expected top-level 'user_id' in response"
    assert "trainingPlanName" in data, "Missing 'trainingPlanName'"
    assert "cards" in data, "Missing 'cards'"
    assert isinstance(data["cards"], list), "'cards' should be a list"
    assert len(data["cards"]) == 10, "Should generate 10 cards"

@pytest.mark.order(2)
def test_generate_training_plan_missing_field():
    """
    1) Submit an incomplete payload (missing 'weight') to /training/generate-plan.
    2) Expect a 422 or 400 response if 'weight' is required in your UserInput model.
    """
    payload = {
        "height": 170.0,
        "age": 25,
        "fitness_level": "Beginner",
        "injury_history": "",
        "target_goal": "Increase stamina"
    }
    response = client.post("/training/generate-plan", json=payload)
    assert response.status_code in [400, 422], (
        f"Expected 400/422 for missing required field, got {response.status_code}"
    )

@pytest.mark.order(3)
@patch("services.training_service.generate_plan_using_openai")
def test_get_training_plan_existing_user(mock_ai):
    """
    1) Mocks AI service -> POST /training/generate-plan
    2) GET /training/plan/{user_id} 
    3) Check user_id, cards, etc. are correct.
    """
    mock_ai.return_value = MOCK_RESPONSE

    creation_payload = {
        "height": 180.0,
        "weight": 80.0,
        "age": 30,
        "fitness_level": "Intermediate",
        "injury_history": "",
        "target_goal": "Lose weight"
    }
    creation_response = client.post("/training/generate-plan", json=creation_payload)
    assert creation_response.status_code == 200, f"POST failed: {creation_response.text}"

    created_data = creation_response.json()
    user_id = created_data["user_id"]

    # Now retrieve the plan
    get_response = client.get(f"/training/plan/{user_id}")
    assert get_response.status_code == 200, "Expected to find the training plan"

    retrieved_data = get_response.json()
    # Check top-level user_id and 'cards'
    assert retrieved_data["user_id"] == user_id, "Mismatched user_id in retrieved plan"
    assert "cards" in retrieved_data, "Missing 'cards' in retrieved plan"
    assert len(retrieved_data["cards"]) == 10, "Expected 10 cards"

@pytest.mark.order(4)
def test_get_training_plan_nonexistent_user():
    """
    1) Attempt GET /training/plan/{user_id} with a random user_id
    2) Expect 404 
    """
    random_user_id = "nonexistent-user-1234"
    response = client.get(f"/training/plan/{random_user_id}")
    assert response.status_code == 404, f"Should return 404, got {response.status_code}"
