import typer
from rich.console import Console
from rich.prompt import Prompt
from langchain_core.messages import HumanMessage, AIMessage

from kaien.agent.graph import app as agent_app
from kaien.memory.db import MemoryEngine
from kaien.config import settings

app = typer.Typer()
console = Console()


@app.command()
def chat():
    """Start an interactive chat session with Kaien."""
    console.print("[bold green]Kaien System Online[/bold green]")
    console.print(f"Model: {settings.model_name} | Shell: {'Enabled' if settings.allow_shell_execution else 'Disabled'}")

    memory = MemoryEngine()
    history = []  # Local session history

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")
        if user_input.lower() in ["exit", "quit"]:
            break

        history.append(HumanMessage(content=user_input))

        # Stream events from the graph
        inputs = {"messages": history}
        final_response = ""

        with console.status("[bold yellow]Kaien is thinking...[/bold yellow]"):
            for event in agent_app.stream(inputs):
                for key, value in event.items():
                    if key == "agent":
                        msg = value["messages"][0]
                        if msg.content:
                            final_response = msg.content
                            console.print(f"[bold green]Kaien[/bold green]: {msg.content}")
                        history.append(msg)
                    elif key == "tools":
                        # Tool outputs are usually handled internally, but we can print logs here
                        pass

        # Save to memory
        if final_response:
            memory.add_interaction(user_input, final_response)


if __name__ == "__main__":
    app()