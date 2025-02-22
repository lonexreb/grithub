# models/training_model.py
from pydantic import BaseModel, Field
from typing import List

class UserInput(BaseModel):
    bmi: float = Field(...)
    daily_exercise: int = Field(...)
    diet_quality: int = Field(...)

class TrainingStep(BaseModel):
    step_number: int
    description: str
    target_difficulty: str
    recommended_duration: int
    simulated_insight: str = Field("")

class TrainingPlan(BaseModel):
    user_id: str
    plan: List[TrainingStep]
