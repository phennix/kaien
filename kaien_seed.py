import os
import asyncio
import subprocess
from typing import List, Optional
import typer
from rich.console import Console
from rich.markdown import Markdown
from litellm import completion
from dotenv import load_dotenv

# Load Environment (API Keys)
load_dotenv()
console = Console()
app = typer.Typer()


# --- 1. The Tools (The Hands) ---
class Tools:
    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Writes content to a file. Creates directories if needed."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def read_file(path: str) -> str:
        """Reads a file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def execute_shell(command: str) -> str:
        """Executes a shell command and returns output."""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        except Exception as e:
            return f"Error executing shell: {str(e)}"


# --- 2. The Brain (The Agent) ---
class ConstructionAgent:
    def __init__(self, model="gpt-4o"):
        self.model = model
        self.history = [
            {"role": "system", "content": """
You are Kaien-Seed, a Construction Agent. 
Your goal is to build the Kaien system based on user instructions and the ARCHITECTURE.md file.
You have access to three tools:
1. write_file(path, content): To create system files.
2. read_file(path): To read the architecture or existing code.
3. execute_shell(command): To run tests or verify files exist.

When asked to build a module, Plan your steps, then Execute them.
Always output your thought process before calling a tool.
Output tool calls in a specific format: ACTION: <tool_name> <args>
"""}
        ]

    async def chat(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})

        # Simple ReAct Loop (Think -> Act -> Observe)
        while True:
            response = completion(
                model=self.model,
                messages=self.history
            )
            content = response.choices[0].message.content
            console.print(f"[bold green]Kaien:[/bold green] {content}")
            self.history.append({"role": "assistant", "content": content})

            # Check for Tool usage (Parsing Logic - Simplified for Seed)
            # In a real impl, we would use proper tool calling APIs or JSON mode
            if "ACTION: write_file" in content:
                # Basic parsing logic for demonstration
                # Real implementation should use Function Calling API
                console.print("[yellow]Detected Write Action... (Parsing implementation required)[/yellow]")
                # Actual parsing and execution logic goes here...
                pass

            # Break if no tool call (Agent is waiting for user)
            if "ACTION:" not in content:
                break


# --- 3. The Interface ---
@app.command()
def start(model: str = "gpt-4o"):
    """Start the Construction Agent."""
    console.print("[bold blue]Kaien Construction Agent Initialized.[/bold blue]")
    agent = ConstructionAgent(model=model)

    # Bootstrap check
    if not os.path.exists("ARCHITECTURE.md"):
        console.print("[red]Warning: ARCHITECTURE.md not found. Please define the vision first.[/red]")

    # Chat Loop
    while True:
        user_in = typer.prompt("You")
        if user_in.lower() in ["exit", "quit"]:
            break
        asyncio.run(agent.chat(user_in))


if __name__ == "__main__":
    app()