# models/gamification_model.py
from pydantic import BaseModel

class GamificationData(BaseModel):
    user_id: str
    xp: int
    level: int
