import os
from litellm import acompletion
from shared.config import Config

class Brain:
    def __init__(self):
        # Default System Prompt to govern behavior
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Kaien, an intelligent AI assistant. "
                "1. If the user asks a question, answer it directly. "
                "2. ONLY use tools if the user explicitly asks for system information or an action. "
                "3. Do not hallucinate tool calls."
            )
        }

    async def think(self, messages: list, tools: list = None):
        """
        Executes the LLM inference.
        """
        # Prepend system prompt to the conversation
        full_history = [self.system_prompt] + messages
        
        print(f"DEBUG: Sending {len(full_history)} messages to model {Config.LLM_MODEL}")

        try:
            response = await acompletion(
                model=Config.LLM_MODEL,
                messages=full_history,
                api_base=Config.LLM_BASE_URL,
                tools=tools,
                tool_choice="auto", # Let model decide between text or tool
            )
            return response
        except Exception as e:
            print(f"CRITICAL LLM ERROR: {e}")
            raise e