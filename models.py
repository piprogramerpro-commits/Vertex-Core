import sqlite3

def init_user_db():
    conn = sqlite3.connect('vertex_users.db')
    c = conn.cursor()
    # status: 0=Pendiente, 1=Validado (Socio), 2=Bloqueado
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT, email TEXT PRIMARY KEY, password TEXT, status INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def register_user(name, email, pwd):
    try:
        conn = sqlite3.connect('vertex_users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (name, email, pwd))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def check_user_status(email):
    conn = sqlite3.connect('vertex_users.db')
    c = conn.cursor()
    c.execute("SELECT status, username FROM users WHERE email=?", (email,))
    result = c.fetchone()
    conn.close()
    return result if result else (None, None)
