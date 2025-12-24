import sqlite3

def init_session_db():
    conn = sqlite3.connect('kaien_sessions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            input TEXT NOT NULL,
            output TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_session_data(input_data: str, output_data: str):
    conn = sqlite3.connect('kaien_sessions.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (input, output) VALUES (?, ?)", (input_data, output_data))
    conn.commit()
    conn.close()

def get_all_sessions():
    conn = sqlite3.connect('kaien_sessions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions ORDER BY timestamp DESC")
    sessions = cursor.fetchall()
    conn.close()
    return sessions
