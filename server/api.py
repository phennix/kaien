"""API endpoints for Kaien Nexus"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import state
import tools.shell_agent as shell_agent
import tools.dev_agent as dev_agent
from schemas import ToolRequest, SessionMessage
import config
import logging

router = APIRouter(prefix="/api/v1")

logger = logging.getLogger(__name__)


# API Endpoints
@router.get("/tools")
async def list_tools():
    """List available tools"""
    return {"tools": list(state.state.tools.keys())}


@router.post("/execute")
async def execute_tool(request: ToolRequest):
    """Execute a tool"""
    tool_name = request.tool
    args = request.args
    
    if tool_name not in state.state.tools:
        return {"error": "Tool not found", "tool": tool_name}
    
    # Check if tool is enabled
    tool_info = state.state.tools[tool_name]
    if not tool_info.get("enabled", True):
        return {"error": "Tool disabled", "tool": tool_name}
    
    # Route to appropriate tool handler
    try:
        if tool_name == "shell":
            if not config.config.get("allow_shell", True):
                return {"error": "Shell commands disabled by configuration", "tool": tool_name}
            
            result = await shell_agent.shell_agent.execute(
                args.get("command"),
                timeout=args.get("timeout", 60),
                cwd=args.get("cwd")
            )
        elif tool_name == "write_file":
            result = dev_agent.dev_agent.write_file(args.get("path"), args.get("content"))
        elif tool_name == "read_file":
            result = dev_agent.dev_agent.read_file(args.get("path"))
        elif tool_name == "list_files":
            result = dev_agent.dev_agent.list_files(args.get("path", "."))
        elif tool_name == "test_code":
            result = dev_agent.dev_agent.test_code(args.get("code"), args.get("language", "python"))
        else:
            result = {"error": "Tool not implemented", "tool": tool_name}
    
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        result = {"error": str(e), "tool": tool_name}
    
    return result


@router.post("/session/message")
async def session_message(message: SessionMessage):
    """Handle session messages"""
    session = state.state.get_session(message.session_id)
    if not session:
        state.state.create_session(message.session_id)
    
    # Log the message
    state.state.log_message(
        message.session_id,
        message.message,
        "",  # Assistant response would go here
        message.metadata or {}
    )
    
    return {"status": "message_logged", "session_id": message.session_id}


@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, limit: int = 50):
    """Get session history"""
    history = state.state.get_session_history(session_id, limit)
    return {"session_id": session_id, "history": history}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    session_id = f"ws_session_{len(state.state.active_sessions) + 1}"
    state.state.create_session(session_id)
    
    logger.info(f"WebSocket session {session_id} connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process message
            response = {
                "session": session_id,
                "message": f"Processed: {message.get('content', '')}",
                "status": "success"
            }
            
            await websocket.send_text(json.dumps(response))
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket session {session_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error in session {session_id}: {str(e)}")
        await websocket.close(code=1011)


# Tool Registration
@router.on_event("startup")
async def register_tools():
    """Register tools on startup"""
    
    logger.info("Registering tools...")
    
    # Register shell tool
    state.state.register_tool({
        "name": "shell",
        "description": "Execute shell commands",
        "parameters": {
            "command": {"type": "string", "required": True},
            "timeout": {"type": "integer", "default": 60},
            "cwd": {"type": "string", "default": None}
        },
        "enabled": config.config.get("modules", {}).get("shell_agent", True)
    })
    
    # Register file operations
    state.state.register_tool({
        "name": "write_file",
        "description": "Write content to a file",
        "parameters": {
            "path": {"type": "string", "required": True},
            "content": {"type": "string", "required": True}
        },
        "enabled": config.config.get("modules", {}).get("dev_agent", True)
    })
    
    state.state.register_tool({
        "name": "read_file",
        "description": "Read content from a file",
        "parameters": {
            "path": {"type": "string", "required": True}
        },
        "enabled": config.config.get("modules", {}).get("dev_agent", True)
    })
    
    state.state.register_tool({
        "name": "list_files",
        "description": "List files in a directory",
        "parameters": {
            "path": {"type": "string", "default": "."}
        },
        "enabled": config.config.get("modules", {}).get("dev_agent", True)
    })
    
    state.state.register_tool({
        "name": "test_code",
        "description": "Test code syntax",
        "parameters": {
            "code": {"type": "string", "required": True},
            "language": {"type": "string", "default": "python"}
        },
        "enabled": config.config.get("modules", {}).get("dev_agent", True)
    })
    
    logger.info(f"Tools registered successfully: {list(state.state.tools.keys())}")