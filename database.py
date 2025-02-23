# database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas using the connection string
client = MongoClient(MONGO_URI)

# Choose the database (you can name it "grithub_db" or any other name)
db = client["grithub_db"]

# Access the collection for training plans
training_collection = db["training_plans"]

# (Optional) You can print out the collection names to verify connection:
if __name__ == "__main__":
    print("Collections in the database:", db.list_collection_names())
