import redis
import os

class VertexMemory:
    def __init__(self):
        # Primero intenta leer la URL de las variables de entorno (para la nube)
        # Si no existe, usa la que me pasaste por defecto
        self.redis_url = os.getenv('REDIS_URL', 'redis://default:ERRLCnrDfYVVagQdSMWywgMaUvkxTvpV@mainline.proxy.rlwy.net:10160')
        try:
            self.db = redis.from_url(self.redis_url, decode_responses=True)
            self.db.ping() # Prueba de conexión
        except Exception as e:
            print(f"Error conectando a Redis: {e}")

    def set_data(self, key, value):
        self.db.set(key, value)

    def get_data(self, key):
        return self.db.get(key)

    def register_device(self, username, hwid, ip):
        user_data = f"{username}|{hwid}|{ip}"
        self.db.hset("vertex_devices", hwid, user_data)
