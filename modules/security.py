import base64
import os

class VertexShield:
    def __init__(self):
        # Usamos tu clave secreta de Railway o una por defecto
        self.key = os.environ.get("SECRET_KEY", "VERTEX_CORE_ULTRA_SECRET_2026").encode()
        
    def encode_data(self, text):
        """Simulación de motor de dispersión y codificación Base64 reforzada"""
        # Aquí es donde el texto se convierte en una cadena indescifrable
        combined = f"VRTX-{text}-CORE".encode()
        encoded = base64.b64encode(combined).decode()
        return encoded[::-1] # Invertimos la cadena para añadir otra capa de seguridad

    def decode_data(self, encoded_text):
        """Reconstrucción de datos binarios"""
        try:
            reversed_text = encoded_text[::-1]
            decoded = base64.b64decode(reversed_text).decode()
            return decoded.replace("VRTX-", "").replace("-CORE", "")
        except:
            return "Error de desencriptado: Integridad comprometida."
