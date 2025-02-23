# services/ai_service.py
import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_plan_using_openai(user_info: dict) -> dict:
    """
    Calls the OpenAI ChatCompletion endpoint with a prompt to generate
    a JSON object containing "trainingPlanName" and "cards".
    Returns the entire JSON object as a Python dict if parsing succeeds,
    or an empty dict if there's an error or unexpected structure.
    """

    prompt = (
        f"You are a professional fitness trainer creating a 20-week workout plan for a user with the following details:\n"
        f"Age: {user_info['age']} years\n"
        f"Height: {user_info['height']} cm\n"
        f"Weight: {user_info['weight']} kg\n"
        f"Fitness Level: {user_info['fitness_level']}\n"
        f"Injury History: {user_info.get('injury_history', '')}\n"
        f"Target Goal: {user_info.get('target_goal', '')}\n\n"
        "Generate valid JSON output where the plan consists of exactly 10 cards, each representing a 2-week (14-day) training block. "
        "Provide a high-level repetitive workout routine for each 2-week block without detailed day-by-day plans, "
        "tailored to the user's fitness level and goals while considering any injury constraints.\n\n"
        "The JSON structure must strictly follow this format:\n"
        "{\n"
        '  "trainingPlanName": "Your Plan Name",\n'
        '  "cards": [\n'
        "    {\n"
        '      "cardNumber": 1,\n'
        '      "title": "Title for Block 1",\n'
        '      "objectives": ["Goal1", "Goal2"],\n'
        '      "routine": [{"exercise": "Push-ups", "sets": 3, "reps": 15, "rest": "60 sec", "description": "Do push-ups"}],\n'
        '      "challenges": ["Challenge1", "Challenge2"]\n'
        "    },\n"
        "    ... 9 more cards ...\n"
        "  ]\n"
        "}\n"
        "Return only valid JSON, strictly adhering to the provided schema, with no additional text."
    )

    messages = [
        {"role": "system", "content": "You are a highly capable assistant that outputs only valid JSON."},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )

    json_output = response.choices[0].message.content.strip()

    try:
        result = json.loads(json_output)
        # Expecting a dict with "trainingPlanName" and "cards".
        if isinstance(result, dict) and "cards" in result:
            return result  # Return the entire dict
        else:
            print("Unexpected JSON structure:", result)
            return {}
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        return {}
