"""Database layer for Kaien system"""

import sqlite3
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from .config import config
import logging

logger = logging.getLogger(__name__)


class KaienDatabase:
    def __init__(self, db_path: str = "kaien.db"):
        self.db_path = db_path
        self._init_tables()
    
    def _init_tables(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Session history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT,
                assistant_message TEXT,
                metadata TEXT
            )
        ''')
        
        # System state
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Tool registry
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                name TEXT PRIMARY KEY,
                description TEXT,
                parameters TEXT,
                enabled INTEGER DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def log_session(self, session_id: str, user_message: str, assistant_message: str, metadata: Optional[Dict] = None):
        """Log a session message"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (session_id, user_message, assistant_message, metadata)
            VALUES (?, ?, ?, ?)
        ''', (
            session_id,
            user_message,
            assistant_message,
            json.dumps(metadata) if metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def get_session_history(self, session_id: str, limit: int = 100) -> List[Dict]:
        """Get session history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT session_id, timestamp, user_message, assistant_message, metadata
            FROM sessions
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "session_id": row[0],
                "timestamp": row[1],
                "user_message": row[2],
                "assistant_message": row[3],
                "metadata": json.loads(row[4]) if row[4] else None
            }
            for row in rows
        ]
    
    def set_state(self, key: str, value: Any):
        """Set system state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO system_state (key, value)
            VALUES (?, ?)
        ''', (key, json.dumps(value)))
        
        conn.commit()
        conn.close()
    
    def get_state(self, key: str) -> Optional[Any]:
        """Get system state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT value FROM system_state WHERE key = ?
        ''', (key,))
        
        row = cursor.fetchone()
        conn.close()
        
        return json.loads(row[0]) if row else None
    
    def register_tool(self, name: str, description: str, parameters: Dict, enabled: bool = True):
        """Register a tool"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO tools (name, description, parameters, enabled)
            VALUES (?, ?, ?, ?)
        ''', (name, description, json.dumps(parameters), 1 if enabled else 0))
        
        conn.commit()
        conn.close()
        logger.info(f"Registered tool in database: {name}")
    
    def get_tools(self) -> List[Dict]:
        """Get all registered tools"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, description, parameters, enabled
            FROM tools
            WHERE enabled = 1
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "name": row[0],
                "description": row[1],
                "parameters": json.loads(row[2]),
                "enabled": bool(row[3])
            }
            for row in rows
        ]