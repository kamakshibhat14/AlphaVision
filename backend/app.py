print("APP.PY IS RUNNING")

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

    # ✅ SESSION SET CORRECTLY
    session["user"] = email

    return jsonify({"message": "Login successful"})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)

    users_collection.insert_one({
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "Signup successful"})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})


def detect_alphabet(image_path):
    from PIL import Image
    import numpy as np

    img = Image.open(image_path).convert("L")
    width, height = img.size
    aspect_ratio = width / height

    pixels = np.array(img)
    avg_brightness = pixels.mean()
    contrast = pixels.std()

    alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Rule buckets (simulation)
    ratio_bucket = int(aspect_ratio * 10) % 7
    brightness_bucket = int(avg_brightness // 20)
    contrast_bucket = int(contrast // 15)

    rule_index = (ratio_bucket + brightness_bucket + contrast_bucket) % 26

    return alphabets[rule_index]


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

