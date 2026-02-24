import redis
import os

class VertexMemory:
    def __init__(self):
        # Intentamos conectar con timeout para que no se bloquee el chat
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        try:
            self.db = redis.from_url(
                redis_url, 
                decode_responses=True, 
                socket_timeout=5,
                retry_on_timeout=True
            )
            print("🟢 Memoria Sincronizada con el Núcleo")
        except Exception as e:
            print(f"🔴 Error de Conexión: {e}")
            self.db = None

    def get_data(self, key):
        if not self.db: return None
        try:
            return self.db.get(key)
        except:
            return None

    def set_data(self, key, value):
        if not self.db: return False
        try:
            self.db.set(key, value)
            return True
        except:
            return False
