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
        # Compute BMI using height (cm) and weight (kg)
        bmi = user_input.weight / ((user_input.height / 100) ** 2)
        user_id = str(uuid.uuid4())

        # Call OpenAI using the computed BMI (daily_exercise and diet_quality not used)
        ai_steps = generate_plan_using_openai(bmi, daily_exercise=0, diet_quality=0)
        plan_steps: List[TrainingStep] = []
        step_number = 1

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
            # Fallback plan
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
        if bmi < 18.5:
            return "low"
        elif 18.5 <= bmi < 25:
            return "medium"
        else:
            return "high"

training_service_instance = TrainingService(repository_instance)
