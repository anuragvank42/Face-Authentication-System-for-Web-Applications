import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    """Establish connection to MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Anu2378chinn@",
            database="mfa_auth_db",
            port=3306
        )
        if conn.is_connected():
            print("✅ MySQL Database Connected Successfully")
        return conn
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
connection = get_db_connection()