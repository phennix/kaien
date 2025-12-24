from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum

class MessageType(str, Enum):
    TOOL_CODE = "tool_code"
    TOOL_RESULT = "tool_result"
    AGENT_THOUGHT = "agent_thought"
    AGENT_RESPONSE = "agent_response"
    USER_INPUT = "user_input"
    ERROR = "error"
    SYSTEM_MESSAGE = "system_message"
    HEARTBEAT = "heartbeat"

class Message(BaseModel):
    type: MessageType
    content: Any
    sender: str
    timestamp: Optional[str] = None # Will be set by the server/client upon creation
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None # For additional context like tool_name, thought_process, etc.
