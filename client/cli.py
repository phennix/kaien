# CLI Client using Typer and Rich
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer()
console = Console()

@app.command()
def interact():
    """Interactive Kaien CLI"""
    console.print(Panel.fit("[bold green]Kaien CLI[/bold green]"))
    console.print("Type 'exit' to quit")
    
    while True:
        user_input = console.input("[bold blue]>>[/bold blue] ")
        if user_input.lower() == "exit":
            break
        console.print(f"[italic]Echo: {user_input}[/italic]")

if __name__ == "__main__":
    app()