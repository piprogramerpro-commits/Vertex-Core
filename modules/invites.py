import sqlite3
import secrets

class VertexInvites:
    def __init__(self, db_path='vertex_vault.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS requests 
                     (email TEXT PRIMARY KEY, status TEXT DEFAULT 'pending', token TEXT)''')
        conn.commit()
        conn.close()

    def request_access(self, email):
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT INTO requests (email) VALUES (?)", (email,))
            conn.commit()
            conn.close()
            return True
        except: return False

    def approve_user(self, email):
        token = secrets.token_hex(8)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE requests SET status='approved', token=? WHERE email=?", (token, email))
        conn.commit()
        conn.close()
        return f"/register/{token}"
