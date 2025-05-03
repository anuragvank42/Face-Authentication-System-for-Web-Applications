# 🧠 Face Authentication System for Web Applications

A full-stack biometric authentication system using real-time **face recognition**, **blink-based and head-movement-based liveness detection**, and **secure image + embedding storage in MySQL**. Designed for modern web applications with a stylish UI, live streaming via MJPEG, and a Python-OpenCV-MediaPipe-Dlib backend.

> 👤 Developed by Anurag Vankadara  
> 🔒 Built for secure, real-time authentication in browser-based apps  
> 🧪 Tested with blink detection, spoof resistance, and MJPEG-based real-time overlays

---

## 📸 Features

- ✅ **Face Registration & Authentication**
- ✅ **Blink-based Liveness Detection** (via Eye Aspect Ratio - EAR)
- ✅ **Head Movement Detection** (for enhanced anti-spoofing)
- ✅ **Real-Time MJPEG Webcam Streaming**
- ✅ **Secure MySQL-based Storage of Face Embeddings & Images (as BLOBs)**
- ✅ **Live Facial Landmarks Overlay on Stream**
- ✅ **Stylish Frontend UI with Blink Count + Liveness Indicators**
- ✅ **REST API endpoints for login, register, and liveness validation**

---

## 🔧 System Architecture

```text
[Web Browser]
    ⇅ MJPEG Stream
[Flask Backend] <—> [Liveness Detection (Blink + Head Movement)]
        ⇅                ⇅
[MediaPipe + Dlib]   [EAR Calculation + Face Mesh]
        ⇅
[Face Embedding + Image Capture]
        ⇅
[MySQL Storage & Retrieval]
```

| Layer      | Technology Used                              |
| ---------- | -------------------------------------------- |
| Frontend   | HTML5, CSS3, JS, Jinja Templates             |
| Backend    | Python, Flask, OpenCV, Dlib, MediaPipe       |
| Liveness   | Blink Detection (EAR), Head Movement Tracker |
| Storage    | MySQL (face embeddings + images as BLOBs)    |
| Streaming  | MJPEG (via Flask `/video_feed` route)        |
| Deployment | Tested on macOS, Linux. Azure-ready setup.   |




##🧠 How It Works
🔹 1. Liveness Detection
Uses MediaPipe to track eye landmarks.

Calculates EAR (Eye Aspect Ratio).

If EAR drops below threshold → blink detected.

Head angle calculated for head-movement liveness.

🔹 2. Face Recognition
Dlib’s face recognition model creates 128D face embeddings.

Stored securely in MySQL alongside original face images.

🔹 3. Real-Time Validation
MJPEG stream shows face mesh + EAR indicators.

Login only succeeds after live liveness check + embedding match.




##🚀 Setup & Run
✅ Prerequisites
Python 3.8+

MySQL Server

Virtual environment tools (venv)

###Installation
git clone https://github.com/anuragvank42/Face-Authentication-System-for-Web-Applications.git
cd face-auth-mfa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt




###Configure MySQL

git clone https://github.com/anuragvank42/Face-Authentication-System-for-Web-Applications.git
cd face-auth-mfa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

###▶️ Run the App
cd backend
python app_1.py


###✅ Roadmap
 MJPEG Webcam Streaming

 Face Embedding via Dlib

 Blink Detection + Liveness Verification

 Store/Match Embeddings in MySQL

 Add email-based 2FA on top

 Dockerize for Cloud Deployment (Azure-ready)

 Integrate with WebRTC stream in browser


📜 License
MIT License.
Feel free to use, fork, and contribute — but give credit 🙏.


PRs welcome. Please open an issue to discuss major changes.
This project was built with ❤️ as a real-time cybersecurity+AI+web systems integration demo.


📬 Contact
📧 anuragvankadara42@gmail.com
📍 Penn State University | M.S Cybersecurity Analytics and Operations

