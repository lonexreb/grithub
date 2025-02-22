# repositories/training_repository.py
from typing import Dict, Optional
from models.training_model import TrainingPlan

class TrainingRepository:
    def __init__(self):
        self._storage: Dict[str, TrainingPlan] = {}

    def save_plan(self, user_id: str, plan: TrainingPlan) -> None:
        self._storage[user_id] = plan

    def get_plan(self, user_id: str) -> Optional[TrainingPlan]:
        return self._storage.get(user_id)

# Create a singleton instance to be reused across the application
repository_instance = TrainingRepository()
