# Define tools in the format expected by LiteLLM/Ollama
SYSTEM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Returns the OS version, platform information, and Python version of the server.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]