from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_user = os.getenv("MONGO_USER")
mongo_pass = os.getenv("MONGO_PASS")
mongo_db = os.getenv("MONGO_DB")

if not mongo_user or not mongo_pass or not mongo_db:
    raise EnvironmentError("Missing one or more MongoDB credentials in environment variables.")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@cluster0.m37al7x.mongodb.net/{mongo_db}?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(mongo_uri)
db = client.get_database(mongo_db)

users_collection = db.users
responses_collection = db.responses
