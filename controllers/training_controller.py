# # controllers/form_advice_controller.py

# import os
# import uuid
# from fastapi import APIRouter, File, UploadFile, Form, HTTPException

# from services.form_advice_service import form_advice_service_instance

# router = APIRouter(prefix="/advice", tags=["Form Advice"])

# @router.post("/evaluate-form")
# async def evaluate_form(
#     prompt: str = Form(...),
#     image: UploadFile = File(...)
# ):
#     """
#     Receives a prompt (text) and an image file. 
#     Calls form_advice_service to generate advice, then returns it.
#     """
#     try:
#         # 1) Save the uploaded image to a temp file
#         temp_filename = f"temp_{uuid.uuid4()}.png"  # or .jpg, etc.
#         with open(temp_filename, "wb") as f:
#             f.write(await image.read())

#         # 2) Call the form advice service
#         advice_text = form_advice_service_instance.generate_advice(prompt, temp_filename)

#         # 3) Remove the temp file
#         os.remove(temp_filename)

#         # 4) Return the advice
#         return {"advice": advice_text}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# controllers/training_controller.py

from fastapi import APIRouter, HTTPException, status
from models.training_model import UserInput, TrainingPlan
from services.training_service import training_service_instance
from database import training_collection

router = APIRouter(prefix="/training", tags=["Training"])

@router.post("/generate-plan", response_model=TrainingPlan)
async def generate_plan(user_input: UserInput):
    """
    POST /training/generate-plan
    """
    try:
        plan = training_service_instance.generate_training_plan(user_input)
        return plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/plan/{user_id}", response_model=TrainingPlan)
async def get_training_plan(user_id: str):
    """
    GET /training/plan/{user_id}
    """
    plan_data = training_collection.find_one({"user_id": user_id})
    if not plan_data:
        raise HTTPException(status_code=404, detail="Training plan not found")
    plan_data.pop("_id", None)
    return plan_data
