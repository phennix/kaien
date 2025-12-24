import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def run():
    console.print("[bold green]Kaien Client CLI is running![/bold green]")
    console.print("This will connect to the Kaien Server via WebSockets.")

if __name__ == "__main__":
    app()