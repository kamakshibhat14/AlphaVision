import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["alphabet_recognition_db"]
users_collection = db["users"]
