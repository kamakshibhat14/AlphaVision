from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create database
db = client["alphabet_recognition_db"]

# Collections
users_collection = db["users"]
detections_collection = db["detections"]
