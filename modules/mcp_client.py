import json
import platform
from modules.brain import Brain
from modules.tools_schema import SYSTEM_TOOLS

class MCPClient:
    def __init__(self):
        self.brain = Brain()
        print("MCP Client Initialized")

    # --- Tool Implementations ---
    def _system_info(self, args: dict = None) -> str:
        """Actual logic for the system_info tool."""
        return f"System: {platform.system()} {platform.release()} | Python: {platform.python_version()}"

    async def process_query(self, query: str) -> str:
        """
        Process a user query: Decides whether to chat or call a tool.
        """
        # 1. Create a FRESH message list (Stateless)
        messages = [{"role": "user", "content": query}]

        # 2. Ask the Brain
        print(f"Processing Query: {query}")
        response = await self.brain.think(messages, tools=SYSTEM_TOOLS)
        
        # 3. Parse Response
        message = response.choices[0].message
        content = message.content or ""
        tool_calls = message.tool_calls

        # 4. Handle Tool Call
        if tool_calls:
            print(f"DEBUG: Model requested tools: {len(tool_calls)}")
            tool_call = tool_calls[0] # Handle first tool only for now
            fn_name = tool_call.function.name
            
            if fn_name == "system_info":
                result = self._system_info()
                return f"Tool Execution Result: {result}"
            else:
                return f"Error: Unknown tool '{fn_name}' requested."
        
        # 5. Handle Text Response
        return content