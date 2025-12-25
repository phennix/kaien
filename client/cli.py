import typer
from rich import print as rprint

app = typer.Typer()

@app.command("hello")
def say_hello(name: str):
    rprint(f"Hello, [bold green]{name}[/bold green]!")

if __name__ == "__main__":
    app()