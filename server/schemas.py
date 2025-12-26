"""Pydantic schemas for Kaien system"""

from pydantic import BaseModel
from typing import Dict, Any, Optional, List


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    enabled: bool = True


class SessionMessage(BaseModel):
    session_id: str
    message: str
    metadata: Optional[Dict] = None


class ToolRequest(BaseModel):
    tool: str
    args: Dict[str, Any]


class FileOperation(BaseModel):
    path: str
    content: Optional[str] = None


class ShellCommand(BaseModel):
    command: str
    timeout: int = 60
    cwd: str = None


class SessionHistoryItem(BaseModel):
    session_id: str
    timestamp: str
    user_message: str
    assistant_message: str
    metadata: Optional[Dict] = None


class SystemState(BaseModel):
    key: str
    value: Any


class MCPToolDefinition(BaseModel):
    """Model Context Protocol tool definition"""
    name: str
    description: str
    parameters: Dict[str, Dict[str, Any]]
    returns: Dict[str, Any]
    enabled: bool = True


class AgentRequest(BaseModel):
    """Request from agent to execute action"""
    agent_id: str
    action: str
    parameters: Dict[str, Any]
    context: Optional[Dict] = None


class AgentResponse(BaseModel):
    """Response from agent action execution"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class SessionCreate(BaseModel):
    """Create a new session"""
    session_id: Optional[str] = None
    initial_context: Optional[Dict] = None


class SessionQuery(BaseModel):
    """Query session information"""
    session_id: str
    limit: int = 50


class SessionState(BaseModel):
    """Session state information"""
    session_id: str
    status: str
    created_at: str
    last_activity: str
    context: Optional[Dict] = None