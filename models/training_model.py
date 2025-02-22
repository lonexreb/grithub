# models/training_model.py
from pydantic import BaseModel, Field
from typing import List

class UserInput(BaseModel):
    bmi: float = Field(..., example=23.5)
    daily_exercise: int = Field(..., example=30, description="Daily exercise in minutes")
    diet_quality: int = Field(..., example=7, description="Scale from 1 (poor) to 10 (excellent)")
    # Add other relevant fields as needed

class TrainingStep(BaseModel):
    step_number: int
    description: str
    target_difficulty: str
    recommended_duration: int  # in minutes
    simulated_insight: str = Field("", description="Physiological simulation output")

class TrainingPlan(BaseModel):
    user_id: str
    plan: List[TrainingStep]
