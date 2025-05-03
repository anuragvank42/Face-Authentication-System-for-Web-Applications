import base64
import cv2
import numpy as np
import mysql.connector
import hashlib
from config import DB_CONFIG
from face_recognition import extract_face_embedding, compare_faces, is_live_face, get_blink_liveness_feedback

latest_mjpeg_frame = None

def update_latest_frame(frame):
    global latest_mjpeg_frame
    latest_mjpeg_frame = frame

def get_latest_frame():
    global latest_mjpeg_frame
    return latest_mjpeg_frame

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("✅ MySQL Database Connected Successfully")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def store_user(username, password, face_embedding, image_bytes):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        encoded_embedding = base64.b64encode(face_embedding.tobytes()).decode('utf-8')
        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (username, password, face_embedding, face_image)
            VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, encoded_embedding, image_bytes))

        conn.commit()
        cursor.close()
        conn.close()

def get_user(username):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, face_embedding FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

def register_user_backend(username, password):
    if get_user(username):
        return False, "User already exists."
    return True, "Please capture face to complete registration."

def authenticate_user_backend(username, password):
    user = get_user(username)
    if not user:
        return False, "User not found."
    if hash_password(password) != user[1]:
        return False, "Incorrect password."
    return True, "Please verify your face to complete login."

def process_face_image_data(_, mode, username, password=None):
    try:
        frame_bgr = get_latest_frame()
        if frame_bgr is None or frame_bgr.shape[0] == 0:
            return {"success": False, "message": "❌ No valid frame found."}

        frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        _ = is_live_face(frame, None)
        blink_count, liveness = get_blink_liveness_feedback()

        if liveness != "Confirmed":
            return {
                "success": False,
                "message": "❌ Liveness not confirmed. Blink at least 5 times.",
                "blink_count": blink_count,
                "liveness": liveness
            }

        embedding = extract_face_embedding(frame)
        if embedding is None:
            return {
                "success": False,
                "message": "❌ No face detected in the frame.",
                "blink_count": blink_count,
                "liveness": liveness
            }

        _, buffer = cv2.imencode('.jpg', frame_bgr)
        image_bytes = buffer.tobytes()

        if mode == "register":
            if password is None:
                return {"success": False, "message": "Password missing during registration."}
            store_user(username, password, embedding, image_bytes)
            return {
                "success": True,
                "message": "✅ Face registered successfully.",
                "blink_count": blink_count,
                "liveness": liveness
            }

        elif mode == "login":
            user = get_user(username)
            if not user:
                return {"success": False, "message": "❌ User not found for login."}
            stored_embedding = np.frombuffer(base64.b64decode(user[2]), dtype=np.float64)
            is_match = bool(compare_faces(embedding, stored_embedding))
            return {
                "success": is_match,
                "message": "✅ Face verified." if is_match else "❌ Face mismatch.",
                "blink_count": blink_count,
                "liveness": liveness
            }

        return {"success": False, "message": "❌ Invalid mode specified."}

    except Exception as e:
        return {"success": False, "message": f"Internal error: {str(e)}"}
