from cryptography.fernet import Fernet
import os

class VertexSecurity:
    def __init__(self):
        # Genera una llave única si no existe
        self.key = os.environ.get("VERTEX_SECRET_KEY", Fernet.generate_key())
        self.cipher = Fernet(self.key)

    def encrypt_msg(self, text):
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt_msg(self, encrypted_text):
        return self.cipher.decrypt(encrypted_text.encode()).decode()

    def anonymize_ip(self, ip_address):
        # Ocultamos la IP del usuario para que sea irrastreable
        parts = ip_address.split('.')
        return f"{parts[0]}.{parts[1]}.xxx.xxx"
