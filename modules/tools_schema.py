"""Tool definitions for LLM tool calling"""

SYSTEM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Get details about the server OS and Python version.",
            "parameters": {}
        }
    }
]