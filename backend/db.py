from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the Mongo URI from environment variables
mongo_uri = os.getenv("MONGO_URI").replace("${MONGO_USER}", os.getenv("MONGO_USER")).replace("${MONGO_PASS}", os.getenv("MONGO_PASS")).replace("${MONGO_DB}", os.getenv("MONGO_DB"))

# Validate the URI
if not mongo_uri:
    raise ValueError("❌ MONGO_URI not found in .env file")

# Connect to MongoDB
client = MongoClient(mongo_uri)

# You can extract the database name from the URI or set it explicitly here:
db = client["virtual_career_assistant"]

# Collections
users_collection = db["users"]
responses_collection = db["responses"]
