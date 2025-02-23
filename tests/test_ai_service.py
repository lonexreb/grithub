# tests/test_ai_service.py
import pytest
from services.ai_service import generate_plan_using_openai

def test_generate_plan_using_openai_returns_dict_with_cards():
    sample_user_info = {
        "age": 25,
        "height": 170,
        "weight": 70,
        "fitness_level": "Beginner",
        "injury_history": "",
        "target_goal": "Build Muscle"
    }
    result = generate_plan_using_openai(sample_user_info)
    
    # We now expect a dict: {"trainingPlanName": "...", "cards": [...]}
    assert isinstance(result, dict), "AI service did not return a dict"
    assert "trainingPlanName" in result, "Missing 'trainingPlanName' key"
    assert "cards" in result, "Missing 'cards' key"
    
    cards = result["cards"]
    assert isinstance(cards, list), "'cards' should be a list"
    assert len(cards) == 10, f"Expected 10 training cards, but got {len(cards)}"
