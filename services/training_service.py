# services/training_service.py
import uuid
from typing import List
from models.training_model import UserInput, TrainingPlan, TrainingStep
from repositories.training_repository import repository_instance
from utils.bio_gears_simulator import simulate_physiology

class TrainingService:
    def __init__(self, repository):
        self.repository = repository

    def generate_training_plan(self, user_input: UserInput) -> TrainingPlan:
        # Create a unique user id for the session (in a real app, use proper user management)
        user_id = str(uuid.uuid4())
        plan_steps: List[TrainingStep] = []

        # Simple rule-based generation logic; in a real scenario, use ML models.
        for i in range(1, 11):
            # Determine target difficulty based on BMI and exercise level (simplified logic)
            if user_input.bmi < 18.5:
                difficulty = "low"
            elif 18.5 <= user_input.bmi < 25:
                difficulty = "medium"
            else:
                difficulty = "high"

            # Simulate physiological insight using our dummy BioGears integration
            simulation = simulate_physiology(difficulty)

            step = TrainingStep(
                step_number=i,
                description=f"Step {i}: Increase exercise intensity gradually.",
                target_difficulty=difficulty,
                recommended_duration=30 + i * 5,  # example: increasing duration per step
                simulated_insight=simulation,
            )
            plan_steps.append(step)

        training_plan = TrainingPlan(user_id=user_id, plan=plan_steps)
        # Save the plan for retrieval
        self.repository.save_plan(user_id, training_plan)
        return training_plan

# Instantiate a service instance using the repository
training_service_instance = TrainingService(repository_instance)
