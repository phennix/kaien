import typer
import logging
from rich.console import Console
from rich.prompt import Prompt
from langchain_core.messages import HumanMessage

# Import the graph (Brain) and Memory
from kaien.agent.graph import app as agent_app
from kaien.memory.db import MemoryEngine
from kaien.config import settings

# Suppress warnings for a cleaner CLI
logging.getLogger("langchain").setLevel(logging.ERROR)
logging.getLogger("chromadb").setLevel(logging.ERROR)

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main_callback():
    """
    Kaien: Ubuntu Agentic AI System.
    """
    pass


@app.command()
def chat():
    """
    Start an interactive chat session with Kaien.
    """
    console.print("[bold green]Kaien System Online[/bold green]")
    console.print(f"Model: {settings.llm.active_provider} | Shell: {'Enabled' if settings.system.allow_shell_execution else 'Disabled'}")

    memory = MemoryEngine()
    history = []  # Local session history

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")
        if user_input.lower() in ["exit", "quit"]:
            break

        history.append(HumanMessage(content=user_input))

        # Stream events from the graph
        inputs = {"messages": history}

        with console.status("[bold yellow]Kaien is thinking...[/bold yellow]"):
            try:
                # We iterate through the stream
                for event in agent_app.stream(inputs):
                    for key, value in event.items():
                        if key == "agent":
                            # The agent returned a message
                            msg = value["messages"][0]
                            if msg.content:
                                console.print(f"[bold green]Kaien[/bold green]: {msg.content}")
                            history.append(msg)
                        elif key == "tools":
                            # Tools executed (optional: log tool output here)
                            pass
            except Exception as e:
                console.print(f"[bold red]Error during execution:[/bold red] {e}")


if __name__ == "__main__":
    app()