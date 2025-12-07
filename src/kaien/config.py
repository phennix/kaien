import os
import yaml
from typing import Optional, Literal
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Sub-configurations for specific providers ---

class OpenAIConfig(BaseModel):
    api_key: Optional[str] = None
    model: str = "gpt-4o"


class GeminiConfig(BaseModel):
    api_key: Optional[str] = None
    model: str = "gemini-3-pro-latest"


class OllamaConfig(BaseModel):
    base_url: str = "http://192.168.0.111:11434"
    # model: str = "llama3"
    model: str = "hf.co/arcee-ai/Trinity-Nano-Preview-GGUF:Q4_K_M"


class LLMSettings(BaseModel):
    active_provider: Literal["openai", "gemini", "ollama"] = "ollama"
    openai: OpenAIConfig = OpenAIConfig()
    gemini: GeminiConfig = GeminiConfig()
    ollama: OllamaConfig = OllamaConfig()


class SystemSettings(BaseModel):
    allow_shell_execution: bool = False
    auto_approve_shell: bool = False
    shell_timeout: int = 60


class StorageSettings(BaseModel):
    data_dir: str = "./data"
    memory_collection_name: str = "kaien_memory"


# --- Main Settings Class ---

class Settings(BaseSettings):
    llm: LLMSettings = LLMSettings()
    system: SystemSettings = SystemSettings()
    storage: StorageSettings = StorageSettings()

    # Allow loading from environment variables (e.g. KAIEN_LLM__OPENAI__API_KEY)
    model_config = SettingsConfigDict(
        env_prefix="KAIEN_",
        env_nested_delimiter="__",
        case_sensitive=False
    )


def load_config(config_path: str = "config.yaml") -> Settings:
    """
    Load settings from YAML, overriding with Environment Variables.
    """
    # Start with defaults
    config_data = {}

    # Load YAML if exists
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            if yaml_data:
                config_data = yaml_data

    # Pydantic will merge: Defaults -> YAML -> Env Vars
    return Settings(**config_data)


# Global settings instance
settings = load_config()