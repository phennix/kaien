import typer
import httpx
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
import json

app = typer.Typer()
console = Console()

# Configuration
SERVER_URL = "http://localhost:8000"

@app.command("hello")
def say_hello(name: str):
    """Say hello to someone"""
    rprint(f"Hello, [bold green]{name}[/bold green]!")

@app.command("tools")
def list_tools():
    """List available tools from the server"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{SERVER_URL}/api/v1/tools")
            response.raise_for_status()
            
            tools = response.json().get("tools", [])
            
            if tools:
                console.print(Panel("Available Tools", style="bold blue"))
                for tool in tools:
                    console.print(f"  - [green]{tool}[/green]")
            else:
                console.print("No tools available", style="yellow")
    
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@app.command("execute")
def execute_tool(
    tool: str = typer.Argument(..., help="Tool name"),
    args_json: str = typer.Option("{}", help="JSON string of arguments")
):
    """Execute a tool on the server"""
    try:
        args = json.loads(args_json)
        
        with httpx.Client() as client:
            response = client.post(
                f"{SERVER_URL}/api/v1/execute",
                json={"tool": tool, "args": args}
            )
            response.raise_for_status()
            
            result = response.json()
            console.print_json(json.dumps(result, indent=2))
    
    except json.JSONDecodeError:
        console.print("Error: Invalid JSON for args", style="red")
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@app.command("shell")
def shell_command(
    command: str = typer.Argument(..., help="Shell command to execute"),
    timeout: int = typer.Option(60, help="Timeout in seconds")
):
    """Execute a shell command via the server"""
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{SERVER_URL}/api/v1/execute",
                json={
                    "tool": "shell",
                    "args": {"command": command, "timeout": timeout}
                }
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                console.print(f"Command: [bold]{command}[/bold]")
                if result.get("stdout"):
                    console.print(Panel(result["stdout"], title="Output", style="green"))
                if result.get("stderr"):
                    console.print(Panel(result["stderr"], title="Error", style="red"))
            else:
                console.print(f"Error: {result.get('error', 'Unknown error')}", style="red")
    
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@app.command("health")
def check_health():
    """Check server health"""
    try:
        with httpx.Client() as client:
            response = client.get(f"{SERVER_URL}/health")
            response.raise_for_status()
            
            health_data = response.json()
            console.print_json(json.dumps(health_data, indent=2))
    
    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

if __name__ == "__main__":
    app()