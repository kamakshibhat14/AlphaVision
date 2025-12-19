from flask import Flask, request, jsonify, session
from flask_cors import CORS
from PIL import Image
from datetime import datetime
from database import users_collection, detections_collection
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_from_directory
from flask import request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "alphabet_secret_key")

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "https://frontend-alphavision.onrender.com"
    ]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    session["user"] = email

    return jsonify({"message": "Login successful"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 409

    hashed_password = generate_password_hash(password)

    users_collection.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Signup successful"}), 201

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


def detect_alphabet(image_path):
    from PIL import Image
    import os
    try:
        img = Image.open(image_path).convert("L")
        width, height = img.size
        aspect_ratio = width / height
        pixels = list(img.getdata())
        avg_brightness = sum(pixels) / len(pixels)
        file_size_kb = os.path.getsize(image_path) / 1024

        score = 0
        if aspect_ratio > 1.2:
            score += 5
        elif aspect_ratio < 0.8:
            score += 10

        if avg_brightness > 180:
            score += 3
        elif avg_brightness < 100:
            score += 7

        if file_size_kb > 200:
            score += 4
        elif file_size_kb < 50:
            score += 8

        alphabets = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return alphabets[score % 26]

    except:
        return "Unknown"

@app.route("/detect", methods=["POST"])
def detect():
    if "user" not in session:
        return jsonify({"message": "Unauthorized access"}), 401

    if "image" not in request.files:
        return jsonify({"message": "Image file missing"}), 400

    image = request.files["image"]
    user = session["user"]

    if image.filename == "":
        return jsonify({"message": "Invalid image file"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    detected_alphabet = detect_alphabet(image_path)

    detections_collection.insert_one({
        "user": session["user"],
        "image_name": image.filename,
        "detected_alphabet": detected_alphabet,
        "timestamp": datetime.now()
    })

    return jsonify({
        "detected_alphabet": detected_alphabet
    })

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/history", methods=["GET"])
def history():
    if "user" not in session:
        return jsonify([])

    records = detections_collection.find({"user": session["user"]})

    history_data = []
    for record in records:
        history_data.append({
            "image_name": record["image_name"],
            "image_url": request.host_url.rstrip("/") + "/uploads/" + record["image_name"],
            "detected_alphabet": record["detected_alphabet"],
            "timestamp": record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(history_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

