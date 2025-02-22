# repositories/training_repository.py
from typing import Dict
from models.training_model import TrainingPlan

class TrainingRepository:
    def __init__(self):
        # Using a simple in-memory storage dictionary
        self._plans: Dict[str, TrainingPlan] = {}

    def save_plan(self, user_id: str, plan: TrainingPlan):
        self._plans[user_id] = plan

    def get_plan(self, user_id: str) -> TrainingPlan:
        return self._plans.get(user_id)

# Instantiate a single repository instance for the app (ensuring DRY)
repository_instance = TrainingRepository()
