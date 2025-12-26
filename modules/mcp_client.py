"""MCP Client - Orchestrator with LLM integration - Phase 3"""

import json
import platform
import logging
from typing import Dict, Any

from modules.brain import Brain
from modules.memory import MemoryModule
from modules.osint import OSINTModule
from modules.tools_schema import SYSTEM_TOOLS

logger = logging.getLogger(__name__)

class MCPClient:
    """Orchestrator that routes queries to LLM and executes tools"""
    
    def __init__(self):
        """Initialize MCP client with brain and modules"""
        self.brain = Brain()
        self.memory = MemoryModule()
        self.osint = OSINTModule()
        logger.info("MCP Client Loaded with Memory & OSINT")
    
    # --- Tool Implementations ---
    def _system_info(self, args: Dict[str, Any] = None) -> str:
        """Get system information"""
        return f"System: {platform.system()} {platform.release()}"
    
    def _remember_info(self, args: Dict[str, Any]) -> str:
        """Store information in memory"""
        text = args.get("text", "")
        if not text:
            return "Error: No text provided to remember"
        return self.memory.remember(text)
    
    def _recall_info(self, args: Dict[str, Any]) -> str:
        """Recall information from memory"""
        query = args.get("query", "")
        if not query:
            return "Error: No query provided for recall"
        return self.memory.recall(query)
    
    async def _run_osint_command(self, args: Dict[str, Any]) -> str:
        """Execute OSINT command"""
        command = args.get("command", "")
        if not command:
            return "Error: No command provided for OSINT"
        return await self.osint.run_command(command)
    
    async def process_query(self, query: str) -> str:
        """
        Process query through LLM and execute tools if requested.
        
        Phase 3 Logic:
        1. Send query to LLM with tool definitions
        2. If LLM requests tool execution, execute it
        3. Otherwise return LLM response directly
        """
        if not query or not isinstance(query, str):
            return "Error: Invalid query"
        
        try:
            # 1. Create a FRESH message list (Stateless)
            messages = [{"role": "user", "content": query}]
            
            # 2. Ask the Brain
            logger.debug(f"Processing Query: {query}")
            response = await self.brain.think(messages, tools=SYSTEM_TOOLS)
            
            # 3. Parse Response
            message = response.choices[0].message
            content = message.content or ""
            tool_calls = getattr(message, 'tool_calls', None)
            
            # 4. Handle Tool Call
            if tool_calls:
                logger.debug(f"DEBUG: Model requested tools: {len(tool_calls)}")
                tool_call = tool_calls[0]  # Handle first tool only for now
                fn_name = tool_call.function.name
                
                try:
                    args = json.loads(tool_call.function.arguments)
                    logger.debug(f"DEBUG: Tool Call -> {fn_name} {args}")
                    
                    if fn_name == "system_info":
                        return f"System: {self._system_info()}"
                    elif fn_name == "remember_info":
                        return self._remember_info(args)
                    elif fn_name == "recall_info":
                        return self._recall_info(args)
                    elif fn_name == "run_osint_command":
                        return await self._run_osint_command(args)
                    else:
                        return f"Error: Unknown tool '{fn_name}'"
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error in tool arguments: {str(e)}")
                    return f"Error: Invalid tool arguments - {str(e)}"
                except Exception as e:
                    logger.error(f"Tool execution error: {str(e)}")
                    return f"Error: Tool execution failed - {str(e)}"
            
            # 5. Handle Text Response
            return content if content else "[No Response]"
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Error: {str(e)}"