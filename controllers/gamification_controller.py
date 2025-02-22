# controllers/gamification_controller.py
from fastapi import APIRouter, HTTPException
from models.gamification_model import GamificationData
from services.gamification_service import gamification_service_instance

router = APIRouter(prefix="/gamification", tags=["Gamification"])

@router.get("/{user_id}", response_model=GamificationData)
async def get_gamification_data(user_id: str):
    data = gamification_service_instance.get_gamification_data(user_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return data

@router.post("/add-xp/{user_id}", response_model=GamificationData)
async def add_xp(user_id: str, xp: int):
    try:
        data = gamification_service_instance.add_xp(user_id, xp)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
