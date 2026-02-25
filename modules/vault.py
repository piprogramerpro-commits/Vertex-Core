import sqlite3

class VertexVault:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (email TEXT PRIMARY KEY, sparks INTEGER, hwid TEXT, role TEXT)''')
        
        # EL ÚNICO COMANDANTE
        admin_email = 'piprogramerpro@gmail.com'
        admin_hwid = 'd16e372dd0bbff1e4806e23e31d82a2ea80095eaeb80754b3d2deea767ee3cb6'
        
        c.execute("INSERT OR REPLACE INTO users (email, sparks, hwid, role) VALUES (?, ?, ?, ?)", 
                  (admin_email, 999999, admin_hwid, 'admin'))
        conn.commit()
        conn.close()

    def check_identity(self, email, current_hwid):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT hwid, role FROM users WHERE email=?", (email.lower().strip(),))
        res = c.fetchone()
        conn.close()
        
        if res:
            saved_hwid, role = res
            if role == 'admin' and saved_hwid == current_hwid:
                return "COMANDANTE"
            if role == 'admin' and saved_hwid != current_hwid:
                return "USUARIO (Intento de Admin fallido)"
            return "USUARIO"
        return "NUEVO"
