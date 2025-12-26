"""State management for Kaien system"""

from typing import Dict, Any, List
import database
import schemas
import config
import logging

logger = logging.getLogger(__name__)


class KaienState:
    def __init__(self):
        self.db = database.KaienDatabase(db_path=config.config.get("db_path", "kaien.db"))
        self.active_sessions: Dict[str, Dict] = {}
        self._load_tools()
    
    def _load_tools(self):
        """Load tools from database"""
        tools_data = self.db.get_tools()
        self.tools = {tool["name"]: tool for tool in tools_data}
        logger.info(f"Loaded {len(self.tools)} tools from database")
    
    def register_tool(self, tool: schemas.ToolDefinition):
        """Register a new tool"""
        tool_dict = tool.dict() if isinstance(tool, schemas.ToolDefinition) else tool
        self.db.register_tool(
            tool_dict["name"],
            tool_dict["description"],
            tool_dict["parameters"],
            tool_dict.get("enabled", True)
        )
        self.tools[tool_dict["name"]] = tool_dict
        logger.info(f"Registered tool: {tool_dict['name']}")
    
    def create_session(self, session_id: str):
        """Create a new session"""
        self.active_sessions[session_id] = {
            "history": [],
            "status": "active",
            "created_at": None
        }
        logger.info(f"Created session: {session_id}")
    
    def get_session(self, session_id: str):
        """Get session information"""
        return self.active_sessions.get(session_id)
    
    def log_message(self, session_id: str, user_message: str, assistant_message: str, metadata: Dict = None):
        """Log a message to session history"""
        if session_id not in self.active_sessions:
            self.create_session(session_id)
        
        self.active_sessions[session_id]["history"].append({
            "user": user_message,
            "assistant": assistant_message,
            "metadata": metadata or {}
        })
        
        # Also log to database
        self.db.log_session(session_id, user_message, assistant_message, metadata)
    
    def get_session_history(self, session_id: str, limit: int = 100) -> List[Dict]:
        """Get session history"""
        return self.db.get_session_history(session_id, limit)
    
    def set_state(self, key: str, value: Any):
        """Set system state"""
        self.db.set_state(key, value)
    
    def get_state(self, key: str, value: Any = None):
        """Get system state"""
        return self.db.get_state(key, value)


# Global state instance
state = KaienState()