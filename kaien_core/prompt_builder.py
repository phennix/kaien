# Constructs the meta-prompts

# kaien_core/prompt_builder.py
from typing import Dict, Any

def build_meta_prompt(user_prompt: str, config: Dict[str, Any]) -> str:
    """Constructs the full meta-prompt for the LLM."""
    system_prompt = config.get('system_prompt', "You are a helpful assistant.")

    # In future phases, this will be dynamically discovered via MCP.
    # For Phase 1, we hardcode the available tools.
    tools_definition = """
    **Available Tools:**
    - `system.Ping()`: Checks if the system extension is online. Returns 'pong'.
    """

    # Combine all parts into the final prompt
    meta_prompt = f"{system_prompt}\n\n{tools_definition}\n\n**User Request:**\n{user_prompt}"
    return meta_prompt