# Defines CLI commands using Click

import os
# Need to adjust sys.path to import from parent directory
import sys

# cli/main.py
import click

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kaien_core.agent import Agent

@click.group()
def cli():
    """Project Kaien Command-Line Interface."""
    pass

@cli.command()
@click.argument('prompt', type=str)
def prompt(prompt):
    """Sends a prompt to the Kaien agent."""
    agent = Agent()
    agent.run(prompt)

if __name__ == '__main__':
    cli()