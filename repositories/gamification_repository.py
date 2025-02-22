# repositories/gamification_repository.py
from typing import Dict, Optional
from models.gamification_model import GamificationData

class GamificationRepository:
    def __init__(self):
        self._data: Dict[str, GamificationData] = {}

    def get_data(self, user_id: str) -> Optional[GamificationData]:
        return self._data.get(user_id)

    def save_data(self, gamification_data: GamificationData) -> None:
        self._data[gamification_data.user_id] = gamification_data

# Create a singleton instance for reuse
gamification_repository_instance = GamificationRepository()
