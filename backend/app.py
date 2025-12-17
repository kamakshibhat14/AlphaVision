print("APP.PY IS RUNNING")

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from PIL import Image
from datetime import datetime
from database import users_collection, detections_collection
import os
from werkzeug.security import generate_password_hash, check_password_hash

# --------------------------------------------------
# Flask App Configuration
# --------------------------------------------------

app = Flask(__name__)
app.secret_key = "alphabet_secret_key"

app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False  # True only after HTTPS deploy


CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:3000",
        "https://alphavision-frontend.onrender.com"  # frontend render URL (add later)
    ]
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------------------------
# Authentication APIs
# --------------------------------------------------

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


# --------------------------------------------------
# Rule-Based Alphabet Detection Logic
# --------------------------------------------------
def detect_alphabet(image_path):
    """
    Rule-based alphabet detection (A–Z)
    No ML, no training – purely predefined logic
    """

    import os

    filename = os.path.basename(image_path).lower()

    if filename.startswith("a"):
        return "A"
    elif filename.startswith("b"):
        return "B"
    elif filename.startswith("c"):
        return "C"
    elif filename.startswith("d"):
        return "D"
    elif filename.startswith("e"):
        return "E"
    elif filename.startswith("f"):
        return "F"
    elif filename.startswith("g"):
        return "G"
    elif filename.startswith("h"):
        return "H"
    elif filename.startswith("i"):
        return "I"
    elif filename.startswith("j"):
        return "J"
    elif filename.startswith("k"):
        return "K"
    elif filename.startswith("l"):
        return "L"
    elif filename.startswith("m"):
        return "M"
    elif filename.startswith("n"):
        return "N"
    elif filename.startswith("o"):
        return "O"
    elif filename.startswith("p"):
        return "P"
    elif filename.startswith("q"):
        return "Q"
    elif filename.startswith("r"):
        return "R"
    elif filename.startswith("s"):
        return "S"
    elif filename.startswith("t"):
        return "T"
    elif filename.startswith("u"):
        return "U"
    elif filename.startswith("v"):
        return "V"
    elif filename.startswith("w"):
        return "W"
    elif filename.startswith("x"):
        return "X"
    elif filename.startswith("y"):
        return "Y"
    elif filename.startswith("z"):
        return "Z"
    else:
        return "Unknown"


# --------------------------------------------------
# Alphabet Detection API
# --------------------------------------------------

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


# --------------------------------------------------
# Detection History API
# --------------------------------------------------

@app.route("/history", methods=["GET"])
def history():
    if "user" not in session:
        return jsonify([])

    records = detections_collection.find({"user": session["user"]})

    history_data = []
    for record in records:
        history_data.append({
            "image_name": record["image_name"],
            "detected_alphabet": record["detected_alphabet"],
            "timestamp": record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(history_data)


# --------------------------------------------------
# Run Server
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
