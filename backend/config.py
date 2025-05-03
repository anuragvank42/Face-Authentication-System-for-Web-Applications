import os

DB_CONFIG = {
    "database": "mfa_auth_db",
    "user": "root",
    "password": "Anu2378chinn@",
    "host": "localhost",
    "port": "3306"
}


# Load encryption key from an environment variable
SECURITY_CONFIG = {
    "encryption_key": os.getenv("ENCRYPTION_KEY")
    
}
