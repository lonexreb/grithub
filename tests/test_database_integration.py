# tests/test_database_integration.py
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import app
from database import training_collection

client = TestClient(app)

# Another stable 10-card plan. 
# Could be identical or slightly different from test_training.py's mock if desired.
MOCK_RESPONSE = {
    "trainingPlanName": "Mock 20-Week Plan",
    "cards": [
        {
            "cardNumber": i,
            "title": f"Block {i}",
            "objectives": [f"Objective {i}"],
            "routine": [
                {
                    "exercise": f"Exercise {i}",
                    "sets": 3,
                    "reps": 10,
                    "rest": "60 sec",
                    "description": f"Routine item for block {i}"
                }
            ],
            "challenges": [f"Challenge {i}-1", f"Challenge {i}-2"]
        }
        for i in range(1, 11)
    ]
}

@pytest.fixture(autouse=True)
def clear_training_collection():
    """
    Before & after each test, clear the 'training_plans' collection to ensure isolation.
    """
    training_collection.delete_many({})
    yield
    training_collection.delete_many({})

@patch("services.training_service.generate_plan_using_openai")
def test_training_plan_database_integration(mock_ai):
    """
    1. POST /training/generate-plan (mock AI) -> expects { user_id, trainingPlanName, cards }
    2. Verify the DB record matches exactly
    3. GET /training/plan/{user_id} and ensure it returns the same data
    """
    # Force the AI service to return a stable 10-card plan
    mock_ai.return_value = MOCK_RESPONSE

    payload = {
        "height": 170,
        "weight": 70,
        "age": 25,
        "fitness_level": "Beginner",
        "injury_history": "",
        "target_goal": "Build Muscle"
    }

    # 1) POST to generate a training plan
    post_response = client.post("/training/generate-plan", json=payload)
    assert post_response.status_code == 200, f"POST failed: {post_response.text}"

    data = post_response.json()
    assert "user_id" in data, "Missing user_id in response"
    assert "trainingPlanName" in data, "Missing trainingPlanName in response"
    assert "cards" in data, "Missing cards in response"
    assert isinstance(data["cards"], list), "cards is not a list"
    assert len(data["cards"]) == 10, f"Expected 10 steps/cards, got {len(data['cards'])}"

    # 2) Check that it's inserted into MongoDB
    user_id = data["user_id"]
    db_record = training_collection.find_one({"user_id": user_id})
    assert db_record is not None, "Training plan not found in the database"

    # Clean up Mongo's _id so we can compare
    db_record.pop("_id", None)
    # The record should match exactly
    assert db_record == data, "Database record does not match the generated training plan"

    # 3) GET /training/plan/{user_id} to confirm the same data is returned
    get_response = client.get(f"/training/plan/{user_id}")
    assert get_response.status_code == 200, f"GET failed: {get_response.text}"
    get_data = get_response.json()
    assert get_data == data, "GET endpoint did not return the same training plan as generated"
