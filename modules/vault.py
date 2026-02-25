import sqlite3
import redis
import os

class VertexVault:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        # Conexión a Redis para velocidad de sesión
        self.redis_url = os.environ.get("REDIS_URL", "redis://default:ERRLCnrDfYVVagQdSMWywgMaUvkxTvpV@redis.railway.internal:6379")
        try:
            self.redis_client = redis.from_url(self.redis_url)
        except:
            self.redis_client = None
            
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (email TEXT PRIMARY KEY, sparks INTEGER, hwid TEXT, role TEXT, status TEXT)''')
        
        # LLAVE MAESTRA REFORZADA
        master_email = 'seguridad_vertex_admin123@gmail.com'
        master_hwid = 'd16e372dd0bbff1e4806e23e31d82a2ea80095eaeb80754b3d2deea767ee3cb6'
        
        # Aseguramos que el Comandante siempre exista con rango 'admin' y estado 'approved'
        c.execute("INSERT OR REPLACE INTO users (email, sparks, hwid, role, status) VALUES (?, ?, ?, ?, ?)", 
                  (master_email, 999999, master_hwid, 'admin', 'approved'))
        conn.commit()
        conn.close()

    def check_access(self, email, hwid):
        email_clean = email.lower().strip()
        
        # Bypass directo por código de seguridad
        if email_clean == 'seguridad_vertex_admin123@gmail.com':
            return "COMMANDER"

        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT role, status FROM users WHERE email=? AND hwid=?", (email_clean, hwid))
        res = c.fetchone()
        conn.close()
        
        if res:
            role, status = res
            if status == 'approved':
                return "USER_APPROVED"
        
        return "PENDING"

    def get_sparks(self, email):
        if email.lower().strip() == 'seguridad_vertex_admin123@gmail.com':
            return "∞"
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT sparks FROM users WHERE email=?", (email.lower().strip(),))
        res = c.fetchone()
        conn.close()
        return res[0] if res else 0
