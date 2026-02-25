import sqlite3
import os

class VertexVault:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users 
                     (email TEXT PRIMARY KEY, sparks INTEGER, role TEXT)''')
        c.execute("INSERT OR IGNORE INTO users VALUES ('gemo@vertex.com', 999999, 'admin')")
        conn.commit()
        conn.close()

    def get_sparks(self, email):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT sparks FROM users WHERE email=?", (email,))
        res = c.fetchone()
        conn.close()
        return res[0] if res else 0

    def use_spark(self, email):
        current = self.get_sparks(email)
        if current > 0:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("UPDATE users SET sparks = sparks - 1 WHERE email=?", (email,))
            conn.commit()
            conn.close()
            return True
        return False

    def add_user(self, email, sparks=10):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, 'user')", (email, sparks))
        conn.commit()
        conn.close()
