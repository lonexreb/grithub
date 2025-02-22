# services/training_service.py
import uuid
from typing import List
from models.training_model import UserInput, TrainingStep, TrainingPlan
from repositories.training_repository import repository_instance
from utils.bio_gears_simulator import simulate_physiology
from services.ai_service import generate_plan_using_openai

class TrainingService:
    def __init__(self, repository):
        self.repository = repository

    def generate_training_plan(self, user_input: UserInput) -> TrainingPlan:
        # Compute BMI from height and weight
        # Assuming height is in centimeters and weight in kilograms
        bmi = user_input.weight / ((user_input.height / 100) ** 2)
        
        # Generate a unique user id
        user_id = str(uuid.uuid4())

        # Use OpenAI API to generate training steps
        ai_steps = generate_plan_using_openai(bmi, 0, 0)
        # Note: Since we no longer have daily_exercise and diet_quality,
        # you might adjust the prompt in ai_service accordingly. Alternatively,
        # you can add default values or compute them based on fitness_level.
        
        plan_steps: List[TrainingStep] = []
        step_number = 1

        # If ai_steps is a valid list of 10 objects, parse them into TrainingStep objects.
        if isinstance(ai_steps, list) and len(ai_steps) == 10:
            for step_data in ai_steps:
                description = step_data.get("description", f"Step {step_number} description not provided.")
                difficulty = step_data.get("difficulty", self._infer_difficulty(bmi))
                duration = step_data.get("duration", 30 + step_number * 5)
                simulation = simulate_physiology(difficulty)
                step = TrainingStep(
                    step_number=step_number,
                    description=description,
                    target_difficulty=difficulty,
                    recommended_duration=duration,
                    simulated_insight=simulation
                )
                plan_steps.append(step)
                step_number += 1
        else:
            # Fallback to a simple rule-based plan if AI call fails or doesn't return 10 steps.
            for i in range(1, 11):
                difficulty = self._infer_difficulty(bmi)
                simulation = simulate_physiology(difficulty)
                step = TrainingStep(
                    step_number=i,
                    description=f"Complete training step {i} with gradual intensity increase.",
                    target_difficulty=difficulty,
                    recommended_duration=30 + i * 5,
                    simulated_insight=simulation
                )
                plan_steps.append(step)
        
        training_plan = TrainingPlan(user_id=user_id, plan=plan_steps)
        self.repository.save_plan(user_id, training_plan)
        return training_plan

    def _infer_difficulty(self, bmi: float) -> str:
        # Example logic: lower BMI might imply lower difficulty and vice versa.
        if bmi < 18.5:
            return "low"
        elif 18.5 <= bmi < 25:
            return "medium"
        else:
            return "high"

# Create a singleton instance for use in controllers
training_service_instance = TrainingService(repository_instance)
