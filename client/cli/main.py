#!/usr/bin/env python3
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def main():
    """Kaien CLI Interface"""
    console.print("[bold green]Kaien CLI Interface[/bold green]")
    console.print("[bold yellow]Welcome to the Kaien System![/bold yellow]")

if __name__ == "__main__":
    app()
