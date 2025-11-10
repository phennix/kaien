# Handles communication with Ollama

# kaien_core/llm_handler.py
import httpx
from typing import Dict, Any

def query_ollama(prompt: str, config: Dict[str, Any]) -> str:
    """Sends a prompt to the Ollama API and returns the response."""
    llm_config = config.get('llm', {})
    url = f"{llm_config.get('host')}/api/generate"
    payload = {
        "model": llm_config.get('model'),
        "prompt": prompt,
        "stream": False,
        "format": "json" # Crucial for getting structured output
    }
    timeout = httpx.Timeout(llm_config.get('request_timeout', 120.0))

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            # The actual response string is inside the 'response' key
            return response.json().get('response', '')
    except httpx.RequestError as e:
        raise Exception(f"Request to Ollama failed: {e}")
    except Exception as e:
        raise Exception(f"An error occurred while querying Ollama: {e}")