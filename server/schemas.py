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