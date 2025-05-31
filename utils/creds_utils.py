import os
import json
from cryptography.fernet import Fernet

CRED_FILE = "saved_creds.json"
KEY_FILE = "key.key"

# --- Key Management ---
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

# --- Save Credentials ---
def save_credentials(email, password):
    key = load_key()
    fernet = Fernet(key)

    encrypted_email = fernet.encrypt(email.encode()).decode()
    encrypted_password = fernet.encrypt(password.encode()).decode()

    with open(CRED_FILE, "w") as f:
        json.dump({
            "email": encrypted_email,
            "password": encrypted_password
        }, f)

# --- Load Credentials ---
def load_credentials():
    if not os.path.exists(CRED_FILE) or not os.path.exists(KEY_FILE):
        return {"email": "", "password": ""}

    key = load_key()
    fernet = Fernet(key)

    with open(CRED_FILE, "r") as f:
        creds = json.load(f)

    try:
        email = fernet.decrypt(creds["email"].encode()).decode()
        password = fernet.decrypt(creds["password"].encode()).decode()
        return {"email": email, "password": password}
    except Exception:
        return {"email": "", "password": ""}
