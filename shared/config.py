"""Configuration module for Kaien system"""

import os
from dotenv import load_dotenv

# Load environment variables from data/.env
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', '.env')
if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

class Config:
    """Central configuration for Kaien system"""
    
    # LLM Configuration
    LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'http://192.168.0.111:11434')
    LLM_MODEL = os.getenv('LLM_MODEL', 'ollama/qwen2.5-coder:32b')
    # LLM_MODEL = os.getenv('LLM_MODEL', 'ollama/ministral-3:14b')

    # Debug mode
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print(f"LLM Base URL: {cls.LLM_BASE_URL}")
        print(f"LLM Model: {cls.LLM_MODEL}")
        print(f"Debug Mode: {cls.DEBUG}")