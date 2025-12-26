"""MCP Client - Orchestrator with LLM integration"""

import json
import platform
import logging
from typing import Dict, Any, Optional

from modules.brain import Brain
from modules.tools_schema import SYSTEM_TOOLS

logger = logging.getLogger(__name__)

class MCPClient:
    """Orchestrator that routes queries to LLM and executes tools"""
    
    def __init__(self):
        """Initialize MCP client with brain"""
        self.brain = Brain()
        self.tools = {}
        self._register_defaults()
        logger.info("MCP Client initialized with LLM integration")
    
    def tool(self, func):
        """Decorator to register a tool."""
        self.tools[func.__name__] = func
        return func
    
    def _register_defaults(self):
        """Register default tools"""
        @self.tool
        def echo(message: str) -> str:
            return f"Echo: {message}"
        
        @self.tool
        def system_info(args: str = "") -> str:
            return f"System: {platform.system()} {platform.release()}"
    
    async def process_query(self, query: str) -> str:
        """
        Process query through LLM and execute tools if requested.
        
        Phase 2 Logic:
        1. Send query to LLM with tool definitions
        2. If LLM requests tool execution, execute it
        3. Otherwise return LLM response directly
        """
        try:
            # Construct messages for LLM
            messages = [
                {"role": "user", "content": query}
            ]
            
            # Call brain with tool definitions
            response = await self.brain.think(messages, tools=SYSTEM_TOOLS)
            
            # Extract the message
            message = response.choices[0].message
            
            # Check if LLM wants to call a tool
            if hasattr(message, 'tool_calls') and message.tool_calls:
                logger.debug(f"LLM requested tool calls: {message.tool_calls}")
                
                # Execute the first tool call (for now)
                tool_call = message.tool_calls[0]
                function_name = tool_call.function.name
                
                # Execute the corresponding function
                if function_name in self.tools:
                    try:
                        # Parse arguments (if any)
                        args = tool_call.function.arguments or ""
                        if args:
                            args_dict = json.loads(args)
                            result = self.tools[function_name](**args_dict)
                        else:
                            result = self.tools[function_name]()
                        
                        return str(result)
                    except Exception as e:
                        logger.error(f"Tool execution error: {str(e)}")
                        return f"Error executing {function_name}: {str(e)}"
                else:
                    return f"Unknown tool: {function_name}"
            
            # Return LLM's text response
            return message.content
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Error: {str(e)}"