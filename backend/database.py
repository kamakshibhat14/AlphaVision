import os
from pymongo import MongoClient

# MongoDB Atlas URI
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://Alphabet:alphabet@cluster0.sjk1p4v.mongodb.net/?appName=Cluster0"

)

client = MongoClient(MONGO_URI)

# Database name (you can keep this)
db = client["alphabet_recognition_db"]

users_collection = db["users"]
detections_collection = db["detections"]
