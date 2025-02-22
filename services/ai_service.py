# services/ai_service.py
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan_using_openai(bmi: float, daily_exercise: int, diet_quality: int) -> str:
    """
    Uses OpenAI to generate a 10-step training plan text.
    Returns a string that we'll parse or display as needed.
    """
    # You can fine-tune this prompt to shape the AI's output format
    prompt = (
    "You are a highly knowledgeable sports coach. "
    "Generate a 10-step progressive training plan. "
    f"User details: BMI={bmi}, daily_exercise={daily_exercise} minutes, diet_quality={diet_quality} on a scale of 1-10. "
    "Each step should have a difficulty, recommended duration in minutes, and a short description. "
    "Return the result as a JSON array of 10 objects, each with the keys: 'description', 'difficulty', and 'duration'."
)


    response = openai.Completion.create(
        engine="gpt-4o",  # or any other model you prefer
        prompt=prompt,
        max_tokens=500,
        temperature=0.7,
        n=1
    )

    return response.choices[0].text.strip()
