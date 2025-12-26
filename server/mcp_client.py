"""Model Context Protocol (MCP) Client for Kaien"""

import json
from typing import Dict, Any, Optional
import httpx
from .schemas import MCPToolDefinition


class MCPClient:
    """Client for interacting with MCP-compatible tool servers"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def get_tools(self) -> Dict[str, MCPToolDefinition]:
        """Get available tools from MCP server"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/tools")
            response.raise_for_status()
            
            tools_data = response.json()
            tools = {}
            
            for tool_name, tool_info in tools_data.items():
                tools[tool_name] = MCPToolDefinition(**tool_info)
            
            return tools
        except Exception as e:
            print(f"Error fetching tools: {str(e)}")
            return {}
    
    async def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool via MCP"""
        try:
            payload = {
                "tool": tool_name,
                "args": args
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/execute",
                json=payload
            )
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name
            }
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
mcp_client = MCPClient()