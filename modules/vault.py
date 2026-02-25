import sqlite3
import redis

class VertexVault:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        self.redis_client = redis.from_url("redis://default:ERRLCnrDfYVVagQdSMWywgMaUvkxTvpV@redis.railway.internal:6379")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (email TEXT PRIMARY KEY, sparks INTEGER, hwid TEXT, role TEXT, status TEXT)''')
        
        # TU ACCESO MAESTRO (BYPASS)
        master_email = 'seguridad_vertex_admin123@gmail.com'
        master_hwid = 'd16e372dd0bbff1e4806e23e31d82a2ea80095eaeb80754b3d2deea767ee3cb6'
        
        c.execute("INSERT OR REPLACE INTO users (email, sparks, hwid, role, status) VALUES (?, ?, ?, ?, ?)", 
                  (master_email, 999999, master_hwid, 'admin', 'approved'))
        conn.commit()
        conn.close()

    def check_access(self, email, hwid):
        # Primero miramos en Redis para velocidad
        cached = self.redis_client.get(f"auth:{email}")
        if cached and cached.decode() == hwid: return "COMMANDER"

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT hwid, role, status FROM users WHERE email=?", (email.lower().strip(),))
        res = c.fetchone()
        conn.close()
        
        if res:
            s_hwid, role, status = res
            if email == 'seguridad_vertex_admin123@gmail.com' and hwid == s_hwid:
                self.redis_client.setex(f"auth:{email}", 3600, hwid)
                return "COMMANDER"
            if status == 'approved': return "USER_APPROVED"
        return "PENDING"

    def get_sparks(self, email):
        if "admin" in email: return "∞"
        return 10 # Sparks por defecto para usuarios
