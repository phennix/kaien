# Main ReAct loop, state management

# kaien_core/agent.py
import json
from . import config as cfg
from . import llm_handler
from . import prompt_builder
from .mcp_client import MCPClient


class Agent:
    def __init__(self):
        self.config = cfg.load_config()

    def run(self, user_prompt: str):
        """Runs the main agent loop for a single turn."""
        print(f"User > {user_prompt}")

        # 1. Build the meta-prompt
        meta_prompt = prompt_builder.build_meta_prompt(user_prompt, self.config)

        # 2. Query the LLM for a decision
        print("\nKaien is thinking...")
        llm_response_str = llm_handler.query_ollama(meta_prompt, self.config)

        try:
            # The LLM is instructed to return a JSON string
            decision = json.loads(llm_response_str)
            tool_to_call = decision.get("tool")
        except json.JSONDecodeError:
            print(f"Kaien > LLM returned a non-JSON response: {llm_response_str}")
            return

        # 3. Execute the decided action
        if tool_to_call == "system.Ping":
            print(f"Kaien > Action: Calling tool `{tool_to_call}`")
            system_ext_config = next((ext for ext in self.config['extensions'] if ext['name'] == 'system'), None)
            if system_ext_config:
                client = MCPClient(system_ext_config['address'])
                result = client.ping_system()
                print(f"Kaien > Result: {result}")
            else:
                print("Kaien > Error: System extension configuration not found.")
        else:
            print(f"Kaien > I have decided not to use a tool or the tool is unknown: {tool_to_call}")