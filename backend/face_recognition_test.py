import cv2
import dlib
import numpy as np
import os
import mediapipe as mp

# Load Dlib models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor(os.path.join(MODEL_DIR, "shape_predictor_68_face_landmarks.dat"))
face_rec_model = dlib.face_recognition_model_v1(os.path.join(MODEL_DIR, "dlib_face_recognition_resnet_model_v1.dat"))

# EAR/Liveness constants
LEFT_EYE_IDXS = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_IDXS = [33, 160, 158, 133, 153, 144]
MOVEMENT_THRESHOLD = 10

# Shared state
calibrated_ear = None
blink_count = 0
consecutive_blinks = 0
blinking_auth_complete = False

# MediaPipe for face landmarks
mp_face_mesh = mp.solutions.face_mesh


def calculate_ear(eye_landmarks):
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    return (A + B) / (2.0 * C)


def is_live_face(frame, prev_landmarks):
    global calibrated_ear, blink_count, consecutive_blinks, blinking_auth_complete

    with mp_face_mesh.FaceMesh(refine_landmarks=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not results.multi_face_landmarks:
            return False, prev_landmarks

        for face_landmarks in results.multi_face_landmarks:
            left_eye = [(int(face_landmarks.landmark[idx].x * frame.shape[1]),
                         int(face_landmarks.landmark[idx].y * frame.shape[0])) for idx in LEFT_EYE_IDXS]
            right_eye = [(int(face_landmarks.landmark[idx].x * frame.shape[1]),
                          int(face_landmarks.landmark[idx].y * frame.shape[0])) for idx in RIGHT_EYE_IDXS]

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            ear = (left_ear + right_ear) / 2.0

            if calibrated_ear is None:
                calibrated_ear = ear
                return False, prev_landmarks

            adaptive_threshold = calibrated_ear * 0.75

            print(f"EAR: {ear:.3f} | Calibrated: {calibrated_ear:.3f} | Threshold: {adaptive_threshold:.3f}")
            print(f"Consecutive: {consecutive_blinks} | Total Blinks: {blink_count}")

            if ear < adaptive_threshold:
                consecutive_blinks += 1
            else:
                if consecutive_blinks >= 2:
                    blink_count += 1
                consecutive_blinks = 0

            if blink_count >= 5:
                blinking_auth_complete = True

            current_landmarks = np.array([
                (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]))
                for lm in face_landmarks.landmark
            ])
            if prev_landmarks is not None:
                movement = np.linalg.norm(current_landmarks - prev_landmarks, axis=1).mean()
                if movement > MOVEMENT_THRESHOLD:
                    return True, current_landmarks
            return False, current_landmarks


def extract_face_embedding(frame):
    faces = detector(frame, 1)
    if len(faces) == 0:
        print("❌ No face detected.")
        return None

    shape = shape_predictor(frame, faces[0])
    return np.array(face_rec_model.compute_face_descriptor(frame, shape))


def compare_faces(embedding1, embedding2, threshold=0.6):
    return np.linalg.norm(embedding1 - embedding2) < threshold


def get_blink_liveness_feedback():
    return blink_count, "Confirmed" if blinking_auth_complete else "Not Confirmed"


def get_blink_and_liveness_status():
    return {
        "blink_count": blink_count,
        "liveness_confirmed": blinking_auth_complete
    }


def reset_liveness_state():
    global calibrated_ear, blink_count, consecutive_blinks, blinking_auth_complete
    calibrated_ear = None
    blink_count = 0
    consecutive_blinks = 0
    blinking_auth_complete = False

def reset_blink_count():
    global blink_count, total_blinks
    blink_count = 0
    total_blinks = 0

