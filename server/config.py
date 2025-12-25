"""Configuration management for Kaien"""

import os
from typing import Dict, Any
from pydantic import BaseModel


class KaienConfig(BaseModel):
    """Main configuration for Kaien system"""
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Database settings
    db_path: str = "kaien.db"
    
    # Security settings
    safe_commands: list = ["ls", "mkdir", "cd", "pwd", "echo", "cat", "grep", "find"]
    allow_shell: bool = True
    
    # LLM settings
    llm_provider: str = "openai"
    llm_model: str = "gpt-4"
    llm_api_key: str = ""
    
    # Module settings
    modules: Dict[str, bool] = {
        "shell_agent": True,
        "dev_agent": True,
        "research_agent": False,
        "osint_agent": False
    }


class ConfigManager:
    """Manage configuration with environment variable overrides"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> KaienConfig:
        """Load configuration from environment variables"""
        config = KaienConfig()
        
        # Override from environment variables
        if "KAIEN_HOST" in os.environ:
            config.host = os.environ["KAIEN_HOST"]
        
        if "KAIEN_PORT" in os.environ:
            config.port = int(os.environ["KAIEN_PORT"])
        
        if "KAIEN_DEBUG" in os.environ:
            config.debug = os.environ["KAIEN_DEBUG"].lower() == "true"
        
        if "KAIEN_DB_PATH" in os.environ:
            config.db_path = os.environ["KAIEN_DB_PATH"]
        
        if "LLM_PROVIDER" in os.environ:
            config.llm_provider = os.environ["LLM_PROVIDER"]
        
        if "LLM_MODEL" in os.environ:
            config.llm_model = os.environ["LLM_MODEL"]
        
        if "LLM_API_KEY" in os.environ:
            config.llm_api_key = os.environ["LLM_API_KEY"]
        
        return config
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        if hasattr(self.config, key):
            return getattr(self.config, key)
        return default
    
    def update(self, key: str, value: Any):
        """Update configuration value"""
        if hasattr(self.config, key):
            setattr(self.config, key, value)


# Global config instance
config = ConfigManager()