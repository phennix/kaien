"""Kaien Nexus - Central orchestration server with MCP integration"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from .state import state
from .config import config
from .mcp_client import mcp_client
from .agent_client import agent_client
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Kaien Nexus",
    version="0.1.0",
    description="Central orchestration server for Kaien autonomous system with MCP support"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routes
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint showing system status"""
    return {
        "status": "Kaien Nexus Online",
        "tools": list(state.tools.keys()),
        "sessions": len(state.active_sessions),
        "modules": config.get("modules", {}),
        "mcp_enabled": True
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tool_count": len(state.tools),
        "session_count": len(state.active_sessions),
        "mcp_status": "connected"
    }


@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "config": config.config.dict(),
        "environment": {
            "host": config.get("host"),
            "port": config.get("port"),
            "debug": config.get("debug")
        }
    }


@app.get("/mcp/tools")
async def mcp_tools():
    """Get MCP-compatible tools"""
    tools = []
    for tool_name, tool_info in state.tools.items():
        tools.append({
            "name": tool_name,
            "description": tool_info.get("description", ""),
            "parameters": tool_info.get("parameters", {})
        })
    
    return {"mcp_tools": tools, "count": len(tools)}


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Kaien Nexus starting up...")
    logger.info(f"Configuration: host={config.get('host')}, port={config.get('port')}")
    logger.info(f"Database: {config.get('db_path')}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Kaien Nexus shutting down...")
    await mcp_client.close()
    await agent_client.close()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.get("host"),
        port=config.get("port"),
        reload=config.get("debug")
    )