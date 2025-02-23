from fastapi import APIRouter, File, UploadFile, Form
import os, uuid

from services.form_advice_service import form_advice_service_instance

router = APIRouter(prefix="/advice", tags=["Form Advice"])

@router.post("/evaluate-form")
async def evaluate_form(prompt: str = Form(...), image: UploadFile = File(...)):
    """
    Endpoint to handle advice generation
    """
    temp_filename = f"temp_{uuid.uuid4()}.jpg"
    with open(temp_filename, "wb") as f:
        f.write(await image.read())

    advice = form_advice_service_instance.generate_advice(prompt, temp_filename)
    os.remove(temp_filename)  # cleanup

    return {"advice": advice}
