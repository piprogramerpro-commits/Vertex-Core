from cryptography.fernet import Fernet
import os

# Generamos o cargamos la llave maestra
# En Railway, deberías poner VERTEX_MASTER_KEY en tus Variables de Entorno
MASTER_KEY = os.environ.get("VERTEX_MASTER_KEY", Fernet.generate_key().decode())
cipher_suite = Fernet(MASTER_KEY.encode())

def encrypt_sensitive_data(text):
    return cipher_suite.encrypt(text.encode()).decode()

def decrypt_sensitive_data(encrypted_text):
    return cipher_suite.decrypt(encrypted_text.encode()).decode()
