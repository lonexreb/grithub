# models/training_model.py
from pydantic import BaseModel
from typing import List, Optional

class UserInput(BaseModel):
    height: float
    weight: float
    age: int
    fitness_level: str
    injury_history: Optional[str] = ""
    target_goal: Optional[str] = ""

class RoutineItem(BaseModel):
    exercise: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    rest: Optional[str] = None
    duration: Optional[str] = None
    intensity: Optional[str] = None
    description: Optional[str] = None

class PlanBlock(BaseModel):
    cardNumber: int
    title: str
    objectives: List[str]
    routine: List[RoutineItem]
    challenges: List[str]

class TrainingPlan(BaseModel):
    user_id: str
    trainingPlanName: str
    cards: List[PlanBlock]