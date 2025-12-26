import os
import json
from litellm import acompletion
from shared.config import Config

class Brain:
    def __init__(self):
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are Kaien, an advanced AI operating system. "
                "1. MODE SELECTION: If the user asks a general question (e.g., 'Why is the sky blue?'), reply in concise, helpful PLAIN TEXT."
                "2. TOOL USE: ONLY output JSON if the user asks to perform an action (e.g., 'Scan this IP', 'Remember this', 'Check system'). "
                "3. FORMAT: Do not wrap plain text answers in JSON. Only wrap tool calls in JSON."
            )
        }

    async def think(self, messages: list, tools: list = None):
        full_history = [self.system_prompt] + messages
        print(f"DEBUG: Sending {len(full_history)} messages to model...")
        try:
            # We force tool_choice='auto' so the model can choose text OR tool
            response = await acompletion(
                model=Config.LLM_MODEL,
                messages=full_history,
                api_base=Config.LLM_BASE_URL,
                tools=tools,
                tool_choice="auto" 
            )
            return response
        except Exception as e:
            print(f"CRITICAL LLM ERROR: {e}")
            raise e