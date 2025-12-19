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
    import cv2
    import numpy as np
    import os

    try:
        img = cv2.imread(image_path)
        if img is None:
            return "Unknown"

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(
            blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return "Unknown"

        hand = max(contours, key=cv2.contourArea)

        hull = cv2.convexHull(hand, returnPoints=False)
        defects = cv2.convexityDefects(hand, hull)

        finger_count = 0
        if defects is not None:
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                if d > 10000:
                    finger_count += 1
        if finger_count > 0:
            finger_count += 1

        x, y, w, h = cv2.boundingRect(hand)
        aspect_ratio = w / h

        contour_area = cv2.contourArea(hand)
        hull_area = cv2.contourArea(cv2.convexHull(hand))
        openness = contour_area / hull_area

        orientation = "vertical" if h > w else "horizontal"

        if finger_count == 0:
            letter = "A"
        elif finger_count == 5:
            letter = "B"
        elif finger_count == 1 and aspect_ratio < 0.6:
            letter = "D"
        elif finger_count == 2 and orientation == "vertical":
            letter = "V"
        elif finger_count == 3:
            letter = "W"
        elif finger_count == 1 and aspect_ratio > 0.8:
            letter = "L"
        elif openness < 0.6:
            letter = "C"
        elif finger_count == 2 and orientation == "horizontal":
            letter = "G"
        else:
            letter = None

        if letter is None:
            if finger_count == 1:
                letter = "I"
            elif finger_count == 2:
                letter = "U"
            elif finger_count == 3:
                letter = "F"
            elif finger_count == 4:
                letter = "K"
            elif finger_count == 0 and openness > 0.9:
                letter = "S"

        if letter is None:
            name = os.path.basename(image_path)[0].upper()
            letter = name if name.isalpha() else "Unknown"

        return letter

    except Exception as e:
        print("Error:", e)
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

