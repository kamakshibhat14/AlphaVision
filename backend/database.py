import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI environment variable not set")

client = MongoClient(MONGO_URI)

db = client["alphabetDB"]

users_collection = db["users"]
detections_collection = db["detections"]
