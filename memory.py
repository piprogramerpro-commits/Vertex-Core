import sqlite3

def init_db():
    conn = sqlite3.connect('vertex_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (user_email TEXT, message TEXT, response TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def save_interaction(email, msg, res):
    conn = sqlite3.connect('vertex_memory.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_email, message, response) VALUES (?, ?, ?)", (email, msg, res))
    conn.commit()
    conn.close()

def get_history(email):
    conn = sqlite3.connect('vertex_memory.db')
    c = conn.cursor()
    c.execute("SELECT message, response FROM chat_history WHERE user_email=? ORDER BY timestamp DESC LIMIT 5", (email,))
    history = c.fetchall()
    conn.close()
    return history
