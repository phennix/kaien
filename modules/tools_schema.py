"""Tool definitions for LLM tool calling - Phase 3"""

SYSTEM_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "system_info",
            "description": "Returns server OS information including platform and release details.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember_info",
            "description": "Save important information or research notes to long-term memory for later retrieval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text content to store in memory"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recall_info",
            "description": "Search long-term memory for relevant information based on a query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant memories"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_osint_command",
            "description": "Execute a shell command for OSINT operations. IMPORTANT: For 'ping', ALWAYS use '-c 4' to limit count. For 'nmap', use '-F' for fast scan. Allowed commands: ping, curl, whois, nslookup, nmap, ls, grep.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The full shell command to execute (e.g., 'ping -c 4 google.com', 'nmap -F scanme.nmap.org')"
                    }
                },
                "required": ["command"]
            }
        }
    }
]