# services/training_service.py
import uuid
from typing import List
from models.training_model import UserInput, TrainingStep, TrainingPlan
from repositories.training_repository import repository_instance
from utils.bio_gears_simulator import simulate_physiology
from services.ai_service import generate_plan_using_openai  # <-- Import AI service

class TrainingService:
    def __init__(self, repository):
        self.repository = repository

    def generate_training_plan(self, user_input: UserInput) -> TrainingPlan:
        user_id = str(uuid.uuid4())

        # 1. Get AI-generated plan text
        ai_plan_text = generate_plan_using_openai(
            user_input.bmi,
            user_input.daily_exercise,
            user_input.diet_quality
        )

        # 2. Parse AI text into steps
        #    For hackathon MVP, we can do a simple line split or bullet split.
        #    In production, you'd want a more robust approach or structured output from the AI.
        lines = [line.strip() for line in ai_plan_text.split('\n') if line.strip()]

        plan_steps: List[TrainingStep] = []
        step_number = 1
        for line in lines:
            # Attempt a naive parse. You can get more fancy with regex or JSON from the AI.
            # Example line might be: "Step 1: Difficulty=medium, Duration=40, Description=Some text"
            # We'll just treat the entire line as the description for the hackathon.
            difficulty = self._infer_difficulty(user_input.bmi)  # Keep or remove your own logic
            simulation = simulate_physiology(difficulty)

            step = TrainingStep(
                step_number=step_number,
                description=line,
                target_difficulty=difficulty,
                recommended_duration=30 + step_number * 5,
                simulated_insight=simulation
            )
            plan_steps.append(step)
            step_number += 1

        training_plan = TrainingPlan(user_id=user_id, plan=plan_steps)
        self.repository.save_plan(user_id, training_plan)
        return training_plan

    def _infer_difficulty(self, bmi: float) -> str:
        if bmi < 18.5:
            return "low"
        elif 18.5 <= bmi < 25:
            return "medium"
        else:
            return "high"

# Create a singleton instance for use in controllers
training_service_instance = TrainingService(repository_instance)
