class MCPClient:
    def __init__(self):
        self.tools = {}
        self._register_defaults()

    def tool(self, func):
        """Decorator to register a tool."""
        self.tools[func.__name__] = func
        return func

    def _register_defaults(self):
        @self.tool
        def echo(message: str) -> str:
            return f"Echo: {message}"
        
        @self.tool
        def system_info(args: str = "") -> str:
            import platform
            return f"System: {platform.system()} {platform.release()}"

    def process_query(self, query: str) -> str:
        """
        Phase 1 Logic: If query starts with '/', treat as tool command.
        Otherwise, just echo.
        """
        if query.startswith("/"):
            parts = query[1:].split(" ", 1)
            tool_name = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            
            if tool_name in self.tools:
                try:
                    return str(self.tools[tool_name](args))
                except Exception as e:
                    return f"Tool Error: {e}"
            return f"Unknown tool: {tool_name}"
        
        # Default Chat Logic (Placeholder for LLM)
        return f"I received your message: '{query}'. (LLM Router not yet active)"