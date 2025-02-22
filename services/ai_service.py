# services/ai_service.py
import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan_using_openai(bmi: float, daily_exercise: int = 0, diet_quality: int = 0) -> list:
    prompt = (
        "You are a highly knowledgeable sports coach. "
        "Generate a 10-step progressive training plan. "
        f"User details: BMI={bmi}. "
        "Each step should have a difficulty, recommended duration in minutes, and a short description. "
        "Return the result as a JSON array of 10 objects with keys: 'description', 'difficulty', and 'duration'."
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
        n=1
    )
    
    json_output = response.choices[0].message.content.strip()
    
    try:
        steps = json.loads(json_output)
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        steps = []
    
    return steps
