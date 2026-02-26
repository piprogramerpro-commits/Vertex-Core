from cryptography.fernet import Fernet

# Generación de la Llave Maestra Vertex (Capa 2)
# En producción, esta llave debería estar en una variable de entorno
def generate_vertex_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

# Protocolo Anti-Cacas
BLACK_LIST = ["elcacas@ejemplo.com"]

def verify_identity(email):
    if email in BLACK_LIST:
        return False
    return True
