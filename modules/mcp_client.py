from flask import Flask
import requests
from rich import print as rprint

def tool(func):
    def wrapper(*args, **kwargs):
        MCPClient.instance().register_tool(func.__name__, func)
        return func(*args, **kwargs)
    return wrapper

class MCPClient:
    _instance = None

    @staticmethod
    def instance():
        if not MCPClient._instance:
            raise Exception('MCPClient is not initialized')
        return MCPClient._instance

    def __init__(self, base_url):
        self.base_url = base_url
        self.registry = {}
        MCPClient._instance = self

    def register_tool(self, tool_name, tool_function):
        self.registry[tool_name] = tool_function

    def send_command(self, command):
        if command in self.registry:
            response = self.registry[command]()
        else:
            url = f"{self.base_url}/command"
            response = requests.post(url, json={"command": command})
            response = response.json()
        return response

if __name__ == "__main__":
    client = MCPClient("http://localhost:8000")

    @tool
    def ping():
        return {"status": "pong"}

    rprint(client.send_command("ping"))