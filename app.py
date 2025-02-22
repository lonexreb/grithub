import os
import time
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the critical environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("Missing environment variable: OPENAI_API_KEY")

# Configure the OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI(title="Workout Plan API", description="API for generating personalized workout plans")

# Add CORS middleware (adjust origins as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict this to your frontend domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend folder as static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve index.html at the root ("/")
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    raise HTTPException(status_code=404, detail="index.html not found")

# --- GET Endpoint for Health Check ---

@app.get("/api/health")
async def health_check():
    """Simple endpoint to check API health."""
    return {"status": "OK"}

# --- POST Endpoint for Generating Workout Plan ---

@app.post("/api/workout")
def get_hardcoded_user_inputs():
    # Hardcoded user input for testing and quick execution
    user_info = {
        'age': 25,
        'height': 175,  # in cm
        'weight': 100,    # in kg
        'current_fitness_level': 'beginner',
        'injury_history': 'none',
        'desired_goals': 'weight loss'
    }
    print("Using hardcoded user inputs:")
    for key, value in user_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    return user_info

def generate_training_plan(user_info):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # Measure total time taken
    total_start_time = time.time()

    prompt = (
        f"You are a professional fitness trainer creating a 20-week workout plan for a user with the following details:\n"
        f"Age: {user_info['age']} years\n"
        f"Height: {user_info['height']} cm\n"
        f"Weight: {user_info['weight']} kg\n"
        f"Current Fitness Level: {user_info['current_fitness_level']}\n"
        f"Injury History: {user_info['injury_history']}\n"
        f"Desired Goals: {user_info['desired_goals']}\n\n"
        f"Generate valid JSON output where the plan consists of 10 cards, each representing a 2-week (14-day) training block. "
        f"Provide a high-level repetitive workout routine for each 2-week block without detailed day-by-day plans. "
        f"The routine should include simple and effective exercises, repeated consistently throughout the block, "
        f"tailored to the user's fitness level and goals while considering any injury constraints.\n\n"
        f"The JSON structure must strictly follow this format:\n"
        f"- 'trainingPlanName': The name of the training plan.\n"
        f"- 'cards': An array of 10 objects, each representing a 2-week block.\n"
        f"- Each card must include:\n"
        f"  - 'cardNumber': The card index (1 to 10).\n"
        f"  - 'title': A brief title for the 2-week training block.\n"
        f"  - 'objectives': A list of key goals for this block.\n"
        f"  - 'routine': A list of 3-5 exercises with sets, reps, rest periods, and descriptions.\n"
        f"  - 'challenges': A list of simple, repetitive challenges for this block.\n\n"
        f"Instructions:\n"
        f"1. Provide exactly 10 cards, each covering a 2-week repetitive training block.\n"
        f"2. Avoid granular day-by-day plans. Instead, focus on a consistent routine for the entire block.\n"
        f"3. Ensure the JSON is complete and valid.\n"
        f"4. Return only valid JSON, strictly adhering to the provided schema.\n"
        f"5. Do not include any code formatting, code block syntax, or additional text."
    )

    messages = [
        {"role": "system", "content": "You are a highly capable assistant that outputs only valid JSON."},
        {"role": "user", "content": prompt}
    ]

    try:
        # Start timer for this request
        start_time = time.time()

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7  # Limit tokens to avoid overly large responses
        )

        json_output = response['choices'][0]['message']['content'].strip()

        print(f"Training plan generated in {time.time() - start_time:.2f} seconds.")

        # Parse the output as JSON
        training_plan = json.loads(json_output)

        # Save the complete training plan to a JSON file
        with open('high_level_training_plan.json', 'w', encoding='utf-8') as f:
            json.dump(training_plan, f, indent=2, ensure_ascii=False)
        print("\nTraining plan successfully saved to 'high_level_training_plan.json'.")
        
        # Pretty print the final training plan
        print("\nGenerated Training Plan:")
        print(json.dumps(training_plan, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        print("Raw output from the API:")
        print(json_output)
    except Exception as e:
        print(f"Error generating the training plan: {e}")

    print(f"\nTotal time taken: {time.time() - total_start_time:.2f} seconds.")

if __name__ == "__main__":
    user_info = get_hardcoded_user_inputs()
    generate_training_plan(user_info)
