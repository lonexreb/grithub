import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
import openai
import time   # <--- Notice we use 'time' in your code for measuring time
import json

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve critical environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not MONGODB_URI or not OPENAI_API_KEY:
    raise Exception("Missing environment variables: MONGODB_URI and/or OPENAI_API_KEY")

# Configure the OpenAI API
openai.api_key = OPENAI_API_KEY

# Initialize FastAPI app
app = FastAPI(
    title="Workout Plan API",
    description="API for generating personalized workout plans"
)

# Optionally add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Mount the frontend folder for static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 2. Serve index.html at the root URL
@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "index.html not found"}

# ==============
# MONGO CLIENT
# ==============
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_default_database()  
collection = db.workout_requests

# ==============
# Pydantic Model
# ==============
class WorkoutRequest(BaseModel):
    height: float = Field(..., description="Height in cm")
    weight: float = Field(..., description="Weight in kg")
    age: int = Field(..., gt=0, description="Age in years")
    currentExerciseLevel: str = Field(..., description="Current exercise level")
    daysToAchieveGoal: int = Field(..., gt=0, description="Days to achieve the desired BMI")
    desiredBMI: float = Field(..., description="Desired BMI")

# ==============
# GET Endpoints
# ==============
@app.get("/api/health")
async def health_check():
    """Simple endpoint to check API health."""
    return {"status": "OK"}

@app.get("/api/workouts")
async def get_workouts():
    """Retrieve all stored workout requests from MongoDB."""
    workouts = []
    cursor = collection.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        workouts.append(document)
    return {"workouts": workouts}

# ==============
# POST Endpoint
# ==============
@app.post("/api/workout")
def generate_training_plan(user_info):
    openai.api_key = openai.api_key = os.getenv('OPENAI_API_KEY')
    
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

# ==============
# Global Handler
# ==============
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# ==============
# Entry Point
# ==============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
