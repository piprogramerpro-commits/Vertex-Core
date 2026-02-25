import sqlite3
import json

class VertexMemory:
    def __init__(self):
        self.db_path = 'vertex_vault.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Tabla para usuarios y sus secretos/preferencias
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (email TEXT PRIMARY KEY, preferences TEXT, sparks INTEGER)''')
        # Tabla para recuerdos a largo plazo
        cursor.execute('''CREATE TABLE IF NOT EXISTS long_term_memory 
                          (email TEXT, insight TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
        conn.close()

    def save_preference(self, email, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT preferences FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        
        prefs = json.loads(row[0]) if row else {}
        prefs[key] = value
        
        cursor.execute("INSERT OR REPLACE INTO users (email, preferences, sparks) VALUES (?, ?, ?)",
                       (email, json.dumps(prefs), 1000)) # 1000 sparks de regalo al empezar
        conn.commit()
        conn.close()

    def get_user_context(self, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT preferences FROM users WHERE email=?", (email,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else {}
