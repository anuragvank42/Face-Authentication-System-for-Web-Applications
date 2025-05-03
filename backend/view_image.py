import cv2
import numpy as np
import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anu2378chinn@",
    database="mfa_auth_db"
)
cursor = conn.cursor()

# Fetch the BLOB data
username = "anuragv42"
cursor.execute("SELECT face_embedding FROM users WHERE username = %s", (username,))
record = cursor.fetchone()

if record:
    blob_data = record[0]  # Extract BLOB
    nparr = np.frombuffer(blob_data, np.uint8)  # Convert to NumPy array
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # Decode image
    
    cv2.imshow("Retrieved Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ No image found.")

# Close connections
cursor.close()
conn.close()
