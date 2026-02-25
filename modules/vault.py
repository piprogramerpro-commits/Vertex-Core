import sqlite3

class VertexVault:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (email TEXT PRIMARY KEY, sparks INTEGER, hwid TEXT, role TEXT, status TEXT)''')
        
        # LLAVE MAESTRA SECRETA
        master_key = 'seguridad_vertex_admin123@gmail.com'
        master_hwid = 'd16e372dd0bbff1e4806e23e31d82a2ea80095eaeb80754b3d2deea767ee3cb6'
        
        c.execute("INSERT OR REPLACE INTO users (email, sparks, hwid, role, status) VALUES (?, ?, ?, ?, ?)", 
                  (master_key, 999999, master_hwid, 'admin', 'approved'))
        conn.commit()
        conn.close()

    def check_access(self, email, current_hwid):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT hwid, role, status FROM users WHERE email=?", (email.lower().strip(),))
        res = c.fetchone()
        conn.close()
        
        if res:
            saved_hwid, role, status = res
            # Validación de la Llave Secreta + HWID
            if email.lower().strip() == 'seguridad_vertex_admin123@gmail.com' and saved_hwid == current_hwid:
                return "COMMANDER"
            if status == 'approved':
                return "USER_APPROVED"
            return "PENDING"
        return "NOT_REGISTERED"

    def get_sparks(self, email):
        if email.lower().strip() == 'seguridad_vertex_admin123@gmail.com':
            return "∞"
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT sparks FROM users WHERE email=?", (email.lower().strip(),))
        res = c.fetchone()
        conn.close()
        return res[0] if res else 10
