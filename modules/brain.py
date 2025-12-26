"""Brain module - LLM adapter for Kaien system"""

from litellm import acompletion
from shared.config import Config
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class Brain:
    """Wrapper around LiteLLM for async chat completions"""
    
    def __init__(self):
        """Initialize brain with configuration"""
        self.config = Config()
        if self.config.DEBUG:
            logger.setLevel(logging.DEBUG)
            logger.debug(f"Brain initialized with model: {self.config.LLM_MODEL}")
    
    async def think(self, messages: List[Dict[str, str]], tools: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process messages through LLM with optional tools"""
        
        # Prepare parameters
        params = {
            "model": self.config.LLM_MODEL,
            "messages": messages,
            "base_url": self.config.LLM_BASE_URL
        }
        
        # Add tools if provided
        if tools:
            params["tools"] = tools
        
        try:
            # Call LiteLLM async completion
            response = await acompletion(**params)
            
            if self.config.DEBUG:
                logger.debug(f"LLM Response: {response}")
            
            return response
        
        except Exception as e:
            logger.error(f"Error in Brain.think: {str(e)}")
            raise
    
    async def chat(self, message: str, system_prompt: str = "You are a helpful AI assistant") -> str:
        """Simple chat interface"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        response = await self.think(messages)
        return response.choices[0].message.content