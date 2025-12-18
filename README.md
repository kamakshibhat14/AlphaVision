# 🔠 AlphaVision – Full-Stack Alphabet Recognition System

AlphaVision is a **full-stack web application** that simulates an **AI-based alphabet recognition system** using **rule-based logic** (no ML training).  
It supports **secure authentication**, **image upload**, **alphabet detection**, and **user-specific detection history**, with complete **frontend–backend integration**.

---

## 🚀 Live Application (Render Deployment)

### 🌐 Frontend (React)
🔗 https://frontend-alphavision.onrender.com

### 🖥 Backend (Flask API)
🔗 https://alphavision-backend.onrender.com

---

## 🎯 Project Objective

To build a **secure and scalable full-stack system** that:
- Allows users to **register and log in**
- Upload an image representing an alphabet (A–Z)
- Detects the alphabet using **backend rule-based logic**
- Stores detection results in **MongoDB Atlas**
- Displays **user-specific detection history**
- Ensures **only authenticated users** can access protected features

---

## 🧩 Key Features

### 🔐 Authentication Module
- User **Signup & Login**
- Passwords stored securely (hashed)
- Session-based authentication
- Logout functionality

### 🔍 Alphabet Detection (Core Feature)
- Upload image (PNG / JPG)
- Backend processes image filename using predefined rules
- Alphabet detected instantly (A–Z)
- No machine learning or training involved

### 📜 Detection History
- History stored in MongoDB Atlas
- Each user sees **only their own detections**
- Shows image name, detected alphabet, date & time
- Displays **“No history found”** if empty

### 🔒 Access Control
- Detection & history pages are **protected**
- Unauthorized access returns proper error responses

---

## 🛠 Tech Stack

### Frontend
- React.js
- Axios
- React Router
- CSS (Custom UI)
- Render (Hosting)

### Backend
- Python
- Flask
- Flask-CORS
- Gunicorn
- Session-based authentication
- Render (Hosting)

### Database
- MongoDB Atlas (Cloud)
- Collections:
  - `users`
  - `detections`

---

## ⚙️ Rule-Based Detection Logic

Alphabet detection is implemented using **filename-based rules**:

```text
a*.jpg → A
b*.png → B
c*.jpg → C
...
z*.png → Z
