# Database Layer: SQLite + ChromaDB
import sqlite3
from pathlib import Path

DB_PATH = Path("data/kaien.db")

class SessionDB:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self._init_tables()
    
    def _init_tables(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state JSON
            )
            """
        )
        self.conn.commit()
    
    def save_session(self, session_id: str, state: dict):
        self.conn.execute(
            """
            INSERT INTO sessions (id, state) VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET state=?, updated_at=CURRENT_TIMESTAMP
            """,
            (session_id, state, state),
        )
        self.conn.commit()
    
    def get_session(self, session_id: str) -> dict:
        cursor = self.conn.execute(
            "SELECT state FROM sessions WHERE id = ?", (session_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else {}

# ChromaDB will be initialized separately for vector memory