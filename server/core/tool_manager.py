from typing import Dict, Type
from server.models import ToolDefinition

class ToolManager:
    def __init__(self):
        self.available_tools: Dict[str, ToolDefinition] = {}

    def register_tool(self, tool_definition: ToolDefinition):
        if tool_definition.name in self.available_tools:
            print(f"Warning: Tool '{tool_definition.name}' already registered. Overwriting.")
        self.available_tools[tool_definition.name] = tool_definition
        print(f"Tool '{tool_definition.name}' registered successfully.")

    def get_tool_definition(self, tool_name: str) -> ToolDefinition:
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self.available_tools[tool_name]

    def list_tools(self) -> Dict[str, ToolDefinition]:
        return self.available_tools

# Example usage (can be removed or moved to tests later)
if __name__ == "__main__":
    manager = ToolManager()

    # Define a sample tool
    shell_tool_def = ToolDefinition(
        name="execute_shell",
        description="Executes a shell command and returns the output.",
        parameters=[
            {"name": "command", "type": "str", "description": "The shell command to execute.", "required": True}
        ],
        code="""import subprocess\ndef execute_shell(command: str):\n    try:\n        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)\n        return {'stdout': result.stdout, 'stderr': result.stderr}\n    except subprocess.CalledProcessError as e:\n        return {'stdout': e.stdout, 'stderr': e.stderr, 'error': str(e)}\n    except Exception as e:\n        return {'stdout': '', 'stderr': '', 'error': str(e)}\n"""
    )

    manager.register_tool(shell_tool_def)

    # Get a tool definition
    tool = manager.get_tool_definition("execute_shell")
    print(f"Retrieved tool: {tool.name}")

    # List all tools
    print("\nAll registered tools:")
    for name, definition in manager.list_tools().items():
        print(f"- {name}: {definition.description}")

