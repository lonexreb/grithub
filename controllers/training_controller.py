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

@router.get("/plan/{user_id}", response_model=TrainingPlan)
async def get_plan(user_id: str):
    plan = training_service_instance.repository.get_plan(user_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Training plan not found")
    return plan
