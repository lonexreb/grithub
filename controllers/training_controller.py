# controllers/training_controller.py
from fastapi import APIRouter, HTTPException, status
from models.training_model import UserInput, TrainingPlan
from services.training_service import training_service_instance
from database import training_collection

router = APIRouter(prefix="/training", tags=["Training"])

@router.post("/generate-plan", response_model=TrainingPlan)
async def generate_plan(user_input: UserInput):
    """
    POST endpoint that:
      1. Takes user input (height, weight, etc.)
      2. Calls training_service to generate a training plan (Pydantic model)
      3. Returns the new structure { user_id, trainingPlanName, cards }
    """
    try:
        plan = training_service_instance.generate_training_plan(user_input)
        return plan  # returns a Pydantic model instance
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/plan/{user_id}", response_model=TrainingPlan)
async def get_training_plan(user_id: str):
    """
    GET endpoint to retrieve a previously generated training plan by user_id.
    If not found, returns 404.
    """
    plan_data = training_collection.find_one({"user_id": user_id})
    if not plan_data:
        raise HTTPException(status_code=404, detail="Training plan not found")
    plan_data.pop("_id", None)
    return plan_data
