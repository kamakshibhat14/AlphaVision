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

    img = cv2.imread(image_path)
    if img is None:
        return "Unknown"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    if not contours:
        return "Unknown"

    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    aspect = w / h if h != 0 else 0

    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    solidity = area / hull_area if hull_area != 0 else 0

    if area < 22000:
        if solidity > 0.9 and 0.9 < aspect < 1.1:
            return "O"
        if aspect < 0.35:
            return "I"
        if 0.55 < aspect < 0.8:
            return "A"
        if aspect > 1.5:
            return "L"
        if solidity < 0.6:
            return "X"
        if 0.8 < aspect < 1.2 and solidity < 0.85:
            return "C"
        if solidity > 0.85 and aspect > 1.2:
            return "D"
        return "E"

    hull_idx = cv2.convexHull(cnt, returnPoints=False)
    defects = cv2.convexityDefects(cnt, hull_idx)

    fingers = 0
    if defects is not None:
        for i in range(defects.shape[0]):
            _, _, _, d = defects[i][0]
            if d > 10000:
                fingers += 1
    if fingers > 0:
        fingers += 1

    if fingers == 0:
        return "A"
    if fingers == 1:
        return "D"
    if fingers == 2:
        return "V"
    if fingers == 3:
        return "W"
    if fingers == 4:
        return "K"
    if fingers == 5:
        return "B"
    if solidity < 0.6:
        return "C"
    if aspect > 1.2:
        return "L"

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

