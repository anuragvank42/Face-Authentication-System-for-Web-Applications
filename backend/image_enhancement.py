import cv2
import numpy as np

# Brightness Threshold (Below this, enhancement is applied)
LOW_LIGHT_THRESHOLD = 80  

def get_brightness(frame):
    """Calculates average brightness of the frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)

def enhance_frame(frame):
    # Convert to grayscale to check brightness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    if brightness < 50:
        # Skip enhancement in dark lighting — return original frame
        return frame

    # Apply CLAHE
    img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_yuv[:, :, 0] = clahe.apply(img_yuv[:, :, 0])
    enhanced = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    # Optional light blur (reduced kernel)
    enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Subtle sharpening
    kernel = np.array([[0, -1, 0],
                       [-1, 5.2, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(enhanced, -1, kernel)

    return sharpened
