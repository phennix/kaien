"""Model Context Protocol (MCP) Client for Kaien Modules"""

import sys
import os
from typing import Dict, Any, Callable, Optional
import httpx
import json

# Add server to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.schemas import MCPToolDefinition


class MCPClient:
    """Client for interacting with MCP-compatible tool servers"""
    
    _instance = None
    
    @staticmethod
    def instance():
        if not MCPClient._instance:
            raise Exception('MCPClient is not initialized')
        return MCPClient._instance
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.registry: Dict[str, Callable] = {}
        self.client = httpx.AsyncClient()
        MCPClient._instance = self
    
    def register_tool(self, tool_name: str, tool_function: Callable):
        """Register a local tool function"""
        self.registry[tool_name] = tool_function
        print(f"Registered tool: {tool_name}")
    
    async def send_command(self, command: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send command to MCP server or execute locally"""
        args = args or {}
        
        # Check if command is registered locally
        if command in self.registry:
            try:
                result = self.registry[command](**args)
                return {
                    "status": "success",
                    "result": result,
                    "source": "local"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "error": str(e),
                    "source": "local"
                }
        
        # Send to remote server
        try:
            payload = {
                "tool": command,
                "args": args
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/execute",
                json=payload
            )
            response.raise_for_status()
            
            return {
                "status": "success",
                "result": response.json(),
                "source": "remote"
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "source": "remote"
            }
    
    async def process_query(self, query: str) -> str:
        """Process a natural language query using MCP"""
        try:
            # Simple query processing - could be enhanced with NLP
            if "tool" in query.lower() or "command" in query.lower():
                # Try to extract tool and args from query
                parts = query.split()
                if len(parts) >= 2:
                    tool_name = parts[1]
                    args = {"query": query}
                    result = await self.send_command(tool_name, args)
                    return json.dumps(result, indent=2)
            
            # Default response
            return json.dumps({
                "status": "info",
                "message": f"Query received: {query}",
                "available_tools": list(self.registry.keys())
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
    
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
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


def tool(func: Callable) -> Callable:
    """Decorator to register a function as an MCP tool"""
    def wrapper(*args, **kwargs):
        # Get the MCP client instance
        client = MCPClient.instance()
        client.register_tool(func.__name__, func)
        return func(*args, **kwargs)
    return wrapper


if __name__ == "__main__":
    # Example usage
    client = MCPClient("http://localhost:8000")
    
    @tool
    def ping():
        return {"status": "pong"}
    
    @tool
    def add(a: int, b: int):
        return {"result": a + b}
    
    # Test local execution
    import asyncio
    
    async def test():
        result = await client.send_command("ping")
        print("Ping result:", result)
        
        result = await client.send_command("add", {"a": 5, "b": 3})
        print("Add result:", result)
        
        # Test query processing
        query_result = await client.process_query("What tools are available?")
        print("Query result:", query_result)
        
        # Test remote execution
        result = await client.send_command("shell", {"command": "ls"})
        print("Shell result:", result)
        
        await client.close()
    
    asyncio.run(test())