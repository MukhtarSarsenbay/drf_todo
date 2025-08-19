from cryptography.fernet import Fernet
import os

TODO_KEY = os.getenv("TODO_KEY")
if not TODO_KEY:
    raise ValueError("TODO_KEY is missing! Add it to your .env file.")

cipher = Fernet(TODO_KEY.encode())

def encrypt_text(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
