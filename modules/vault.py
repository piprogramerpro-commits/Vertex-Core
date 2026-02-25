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
        
        # IDENTIDAD ÚNICA DEL COMANDANTE GEMO
        admin_email = 'piprogramerpro@gmail.com'
        admin_hwid = 'd16e372dd0bbff1e4806e23e31d82a2ea80095eaeb80754b3d2deea767ee3cb6' 
        
        # Insertamos o actualizamos al admin con su HWID maestro
        c.execute("INSERT OR IGNORE INTO users (email, sparks, hwid, role) VALUES (?, ?, ?, 'admin')", 
                  (admin_email, 999999, admin_hwid))
        conn.commit()
        conn.close()

    def check_identity(self, email, current_hwid):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT hwid, role FROM users WHERE email=?", (email.lower(),))
        res = c.fetchone()
        conn.close()
        
        if res:
            saved_hwid, role = res
            if role == 'admin' and saved_hwid == current_hwid:
                return "ADMIN_CONFIRMED"
            elif role == 'admin' and saved_hwid != current_hwid:
                return "IMPOSTOR"
            return "USER_AUTH"
        return "NEW_USER"

    def get_sparks(self, email):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT sparks FROM users WHERE email=?", (email.lower(),))
        res = c.fetchone()
        conn.close()
        return res[0] if res else 0

    def use_spark(self, email):
        current = self.get_sparks(email)
        if current > 0:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE users SET sparks = sparks - 1 WHERE email=?", (email.lower(),))
            conn.commit()
            conn.close()
            return True
        return False
