from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify, session
from user_manager import register_user_backend, authenticate_user_backend, process_face_image_data, update_latest_frame
from face_recognition import get_blink_and_liveness_status, is_live_face, reset_liveness_state, reset_blink_count
import cv2

app = Flask(__name__)
app.secret_key = "secure_key_123"

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, message = authenticate_user_backend(username, password)
        flash(message, "success" if success else "danger")
        if success:
            session["username"] = username
            session["mode"] = "login"
            return redirect(url_for("camera_preview"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        success, message = register_user_backend(username, password)
        flash(message, "success" if success else "danger")
        if success:
            session["username"] = username
            session["password"] = password
            session["mode"] = "register"
            return redirect(url_for("camera_preview"))
    return render_template("register.html")

@app.route("/camera")
def camera_preview():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("camera_preview.html")

@app.route("/capture_face", methods=["POST"])
def capture_face():
    data = request.get_json()
    username = session.get("username")
    mode = session.get("mode")

    if mode == "register":
        password = session.get("password")
        result = process_face_image_data(data.get("image"), mode="register", username=username, password=password)
        session.pop("password", None)
    elif mode == "login":
        result = process_face_image_data(data.get("image"), mode="login", username=username)
    else:
        result = {"success": False, "message": "Unknown session mode."}
        return jsonify(result)

    if result.get("success"):
        reset_blink_count()

    status = get_blink_and_liveness_status()
    result["blink_count"] = status["blink_count"]
    result["liveness"] = "Confirmed" if status["liveness_confirmed"] else "Not Confirmed"
    return jsonify(result)

@app.route("/reset_liveness", methods=["POST"])
def reset_liveness():
    reset_liveness_state()
    return jsonify({"status": "Liveness reset done ✅"})

@app.route("/get_status", methods=["GET"])
def get_status():
    return jsonify(get_blink_and_liveness_status())

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/video_feed")
def video_feed():
    def generate():
        cap = cv2.VideoCapture(0)
        prev_landmarks = None
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    break
                _, prev_landmarks = is_live_face(frame, prev_landmarks)
                update_latest_frame(frame.copy())
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        finally:
            reset_blink_count()
            cap.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
