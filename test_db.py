# test_db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

try:
    db = client.get_database("grithub_db")  # Use your chosen database name
    print("Collections in the database:", db.list_collection_names())
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")
