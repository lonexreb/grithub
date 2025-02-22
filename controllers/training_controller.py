# controllers/training_controller.py
from fastapi import APIRouter, HTTPException
from models.training_model import UserInput, TrainingPlan
from services.training_service import training_service_instance

router = APIRouter(prefix="/training", tags=["Training"])

@router.post("/generate-plan", response_model=TrainingPlan)
async def generate_plan(user_input: UserInput):
    try:
        training_plan = training_service_instance.generate_training_plan(user_input)
        return training_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
