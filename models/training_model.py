from pydantic import BaseModel, Field
from typing import List

class UserInput(BaseModel):
    height: float   # in centimeters
    weight: float   # in kilograms
    age: int
    fitness_level: str
    injury_history: str = Field("", description="Optional injury history")
    target_goal: str = Field("", description="Optional target goal")

class TrainingStep(BaseModel):
    step_number: int
    description: str
    target_difficulty: str
    recommended_duration: int  # in minutes
    simulated_insight: str = Field("")

class TrainingPlan(BaseModel):
    user_id: str
    plan: List[TrainingStep]
