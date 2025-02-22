import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan_using_openai(bmi: float, daily_exercise: int, diet_quality: int) -> list:
    user_prompt = (
        "Generate a 10-step progressive training plan. "
        f"User details: BMI={bmi}, daily_exercise={daily_exercise} minutes, diet_quality={diet_quality} on a scale of 1-10. "
        "Each step should have a difficulty, recommended duration in minutes, and a short description. "
        "Return the result as a JSON array of 10 objects, each with the keys: 'description', 'difficulty', and 'duration'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a highly knowledgeable sports coach."},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=500,
        temperature=0.7,
        n=1
    )
    
    json_output = response.choices[0].message["content"].strip()
    
    try:
        steps = json.loads(json_output)
    except json.JSONDecodeError as e:
        # In case of a parsing error, log and return an empty list or fallback value
        print("JSON parsing error:", e)
        steps = []
    
    return steps
