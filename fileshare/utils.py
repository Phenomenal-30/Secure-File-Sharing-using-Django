from cryptography.fernet import Fernet
from django.conf import settings

# Use a constant key for encryption/decryption
FERNET_SECRET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_SECRET_KEY)

def encrypt_file_id(file_id):
    return fernet.encrypt(str(file_id).encode()).decode()

def decrypt_file_id(token):
    return int(fernet.decrypt(token.encode()).decode())
