# src/kaien/tools/system.py
import subprocess
import os
from langchain_core.tools import tool
from kaien.config import settings


@tool
def execute_shell(command: str) -> str:
    """
    Executes a shell command on the Ubuntu system.
    Use this to list files (ls), check processes (ps), or install packages (apt/pip).
    """
    if not settings.system.allow_shell_execution:
        return "Error: Shell execution is disabled in configuration."

    try:
        # Run with timeout defined in config
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=settings.system.shell_timeout
        )
        # Combine output for the LLM
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
        if not output:
            output = "Command executed successfully (no output)."

        return output
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {settings.system.shell_timeout} seconds."
    except Exception as e:
        return f"Execution failed: {str(e)}"


@tool
def read_file(file_path: str) -> str:
    """Reads the content of a file from the local filesystem."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Overwrites if it exists."""
    if not settings.system.allow_shell_execution:
        # Writing files is also dangerous, so we gate it with the shell permission
        return "Error: File writing is disabled (requires shell execution permission)."

    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"