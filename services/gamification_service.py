# services/gamification_service.py
from models.gamification_model import GamificationData
from repositories.gamification_repository import gamification_repository_instance

class GamificationService:
    def __init__(self, repository):
        self.repository = repository

    def add_xp(self, user_id: str, xp_to_add: int) -> GamificationData:
        # Retrieve existing gamification data or create new if not exists
        data = self.repository.get_data(user_id)
        if data is None:
            data = GamificationData(user_id=user_id, xp=0, level=1)
        # Increase XP
        data.xp += xp_to_add
        # For simplicity: Level up for every 100 XP
        data.level = data.xp // 100 + 1
        self.repository.save_data(data)
        return data

    def get_gamification_data(self, user_id: str) -> GamificationData:
        data = self.repository.get_data(user_id)
        if data is None:
            # If no data exists, initialize it
            data = GamificationData(user_id=user_id, xp=0, level=1)
            self.repository.save_data(data)
        return data

# Create a singleton instance for use in controllers
gamification_service_instance = GamificationService(gamification_repository_instance)
