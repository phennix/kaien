import os
import json
import asyncio
import subprocess
import re
import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from litellm import completion
from dotenv import load_dotenv

# Load Environment
load_dotenv()
console = Console()
app = typer.Typer()

# --- Configuration ---
DEFAULT_MODEL = "ollama/qwen2.5-coder:32b"
# DEFAULT_MODEL = "ollama/ministral-3:8b"
# DEFAULT_MODEL = "ollama/ministral-3:14b"
# DEFAULT_MODEL = "ollama/mistral-small3.2:24b"
# DEFAULT_MODEL = "ollama/nemotron-3-nano:30b"
# DEFAULT_MODEL = "ollama/cogito:32b"
# DEFAULT_MODEL = "ollama/qwen3:14b"
# DEFAULT_MODEL = "ollama/qwen2.5-coder:14b"
# DEFAULT_MODEL = "ollama/qwen2.5-coder:7b"
# DEFAULT_MODEL = "ollama/embeddinggemma:300m"

API_BASE = "http://192.168.0.111:11434"

# --- 1. The Tools (The Hands) ---
class Tools:
    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Writes content to a file. Creates directories automatically."""
        try:
            # Security check
            if ".." in path or path.startswith("/"):
                return "Error: Path must be relative to current directory."

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Success: Wrote {len(content)} bytes to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    @staticmethod
    def read_file(path: str) -> str:
        """Reads a file."""
        try:
            if not os.path.exists(path):
                return f"Error: File {path} does not exist."
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def execute_shell(command: str) -> str:
        """Executes a shell command."""
        console.print(f"[bold red]AGENT WANTS TO RUN:[/bold red] {command}")
        # Auto-confirm for ls and mkdir to speed up scaffolding
        if not (command.startswith("ls") or command.startswith("mkdir")):
            confirm = typer.confirm("Allow this command?")
            if not confirm:
                return "Error: User denied command execution."

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=60
            )
            output = result.stdout + result.stderr
            return output if output else "Success: Command executed (no output)."
        except Exception as e:
            return f"Error executing shell: {str(e)}"


# --- 2. The Brain (The Agent) ---
class SeedAgent:
    def __init__(self, model):
        self.model = model
        self.tools = Tools()
        self.system_prompt = """You are Kaien-Seed, an autonomous construction agent.
            Your goal is to build the Kaien system by reading the 'ARCHITECTURE.md' and writing Python code.
            
            You have access to tools. To use a tool, you MUST output a JSON block strictly in this format:
            
            ```json
            {
                "tool": "write_file",
                "args": {
                    "path": "server/main.py",
                    "content": "print('hello')"
                }
            }
            ```
            
            Available Tools:
                write_file(path, content) - Create code files.
                read_file(path) - Read requirements or code.
                execute_shell(command) - Create folders (mkdir) or list files (ls).
            IMPORTANT RULES:
            1. Only return ONE tool call per turn.
            2. DO NOT write conversational text like "Here is the code". Just output the JSON.
            3. If you need to read a file to understand what to do, use read_file first.
            4. If the task is finished, output "DONE".
            """
        self.history = [{"role": "system", "content": self.system_prompt}]

    # def _extract_json_tool(self, content: str):
    #     """Robust Regex-based parsing for local model output"""
    #     try:
    #         # 1. Regex to find content between json and or just { ... }
    #         json_match = re.search(r"(?:json)?\s*(\{.*?\})\s*", content, re.DOTALL)
    #
    #         if json_match:
    #             json_str = json_match.group(1)
    #         else:
    #             # Fallback: Look for the first outer bracket pair if markdown is missing
    #             json_match = re.search(r"(\{.*\})", content, re.DOTALL)
    #             if json_match:
    #                 json_str = json_match.group(1)
    #             else:
    #                 return None
    #
    #         return json.loads(json_str)
    #     except Exception as e:
    #         console.print(f"[dim red]JSON Parsing Error: {e}[/dim red]")
    #         return None

    def _extract_json_tool(self, content: str):
        """Robust parsing for local model output"""
        try:
            # 1. Try finding markdown json blocks
            if "json" in content: # Split byjson and take the second part, then split by json_str = content.split("json")[1].split("")[0].strip() elif "" in content:
            # Sometimes models forget 'json' but use backticks
                json_str = content.split("```json")[1].split("```")[0].strip()
            else:
            # 2. Fallback: Try finding raw JSON structure
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end != -1:
                    json_str = content[start:end]
                else:
                    return None

            return json.loads(json_str)
        except Exception as e:
             # console.print(f"[dim]JSON Parsing failed: {e}[/dim]")
             return None


    async def chat(self, user_input: str):
        self.history.append({"role": "user", "content": user_input})

        step_count = 0
        max_steps = 15

        while step_count < max_steps:
            console.print("[dim]Thinking...[/dim]")

            try:
                response = completion(
                    model=self.model,
                    messages=self.history,
                    api_base=API_BASE,
                    stream=False,
                    timeout=600
                )
            except Exception as e:
                console.print(f"[bold red]LLM Connection Error:[/bold red] {e}")
                return

            content = response.choices[0].message.content or ""

            # DEBUG: Print what the model actually said
            # console.print(Panel(content, title="Raw Model Output", border_style="blue"))
            console.print(content)

            self.history.append({"role": "assistant", "content": content})

            if "DONE" in content:
                console.print("[bold green]Agent signaled completion.[/bold green]")
                break

            # Parse Tool
            tool_data = self._extract_json_tool(content)

            if tool_data:
                tool_name = tool_data.get("tool")
                args = tool_data.get("args", {})

                result = "Unknown Tool"
                if tool_name == "write_file":
                    console.print(f"[cyan]Writing file:[/cyan] {args.get('path')}")
                    result = self.tools.write_file(args.get("path"), args.get("content"))
                elif tool_name == "read_file":
                    console.print(f"[cyan]Reading file:[/cyan] {args.get('path')}")
                    result = self.tools.read_file(args.get("path"))
                elif tool_name == "execute_shell":
                    console.print(f"[cyan]Shell cmd:[/cyan] {args.get('command')}")
                    result = self.tools.execute_shell(args.get("command"))

                console.print(f"[dim]Result: {str(result)[:200]}...[/dim]")
                self.history.append({"role": "user", "content": f"Observation: {result}"})
            else:
                # If no tool found, break to ask user for guidance
                console.print("[yellow]No tool call detected. Waiting for user...[/yellow]")
                break

            step_count += 1

    # --- 3. Entry Point ---

@app.command()
def start():
    """Start the Kaien Construction Site."""

    console.rule("[bold blue]Kaien Construction Site (Ollama)[/bold blue]")
    console.print(f"Using Model: [green]{DEFAULT_MODEL}[/green]")
    console.print(f"API Base: [green]{API_BASE}[/green]")
    agent = SeedAgent(model=DEFAULT_MODEL)

    # Initial Check
    if not os.path.exists("ARCHITECTURE.md"):
        console.print("[yellow]Hint: Create an ARCHITECTURE.md file to guide the agent.[/yellow]")

    while True:
        try:
            user_in = typer.prompt("User")
            if user_in.lower() in ["exit", "quit"]:
                break
            asyncio.run(agent.chat(user_in))
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    app()
