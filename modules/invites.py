import secrets
import sqlite3

class VertexInvites:
    def __init__(self, db_path='vertex_vault.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS invites 
                     (token TEXT PRIMARY KEY, used INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()

    def generate_token(self):
        token = secrets.token_hex(8)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO invites (token) VALUES (?)", (token,))
        conn.commit()
        conn.close()
        return token

    def validate_token(self, token):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT used FROM invites WHERE token=?", (token,))
        res = c.fetchone()
        if res and res[0] == 0:
            c.execute("UPDATE invites SET used = 1 WHERE token=?", (token,))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
