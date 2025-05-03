from cryptography.fernet import Fernet
from config import SECURITY_CONFIG

cipher_suite = Fernet(SECURITY_CONFIG['encryption_key'])

def encrypt_data(data):
    return cipher_suite.encrypt(data)

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data)
