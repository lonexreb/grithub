# services/training_service.py

import uuid
from typing import Dict, Any

from models.training_model import UserInput, TrainingPlan
from repositories.training_repository import repository_instance
from services.ai_service import generate_plan_using_openai
from database import training_collection


class TrainingService:
    def __init__(self, repository):
        self.repository = repository

    def generate_training_plan(self, user_input: UserInput) -> TrainingPlan:
        """
        1) Convert user input to a dict
        2) Call AI to get {trainingPlanName, cards}
        3) Build a Pydantic TrainingPlan model
        4) Insert the dict version into DB
        5) Return the Pydantic model so your controller can respond
        """
        user_info = user_input.dict()
        ai_result = generate_plan_using_openai(user_info)

        # Generate a unique user_id
        user_id = str(uuid.uuid4())

        # Build a Pydantic TrainingPlan model so the DB doc matches the final response
        plan_instance = TrainingPlan(
            user_id=user_id,
            trainingPlanName=ai_result.get("trainingPlanName", "Default Name"),
            cards=ai_result.get("cards", [])
        )

        # Convert to dict for storing in-memory and in MongoDB
        plan_dict = plan_instance.dict()
        self.repository.save_plan(user_id, plan_dict)
        training_collection.insert_one(plan_dict)

        # Return the Pydantic model (FastAPI auto-converts it to JSON in your controller)
        return plan_instance


# IMPORTANT: define a single instance that other files can import
training_service_instance = TrainingService(repository_instance)