# src/kaien/agent/factory.py
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from kaien.config import settings


def get_llm() -> BaseChatModel:
    """Returns the configured Chat Model based on config.yaml."""
    provider = settings.llm.active_provider

    if provider == "openai":
        return ChatOpenAI(
            api_key=settings.llm.openai.api_key,
            model=settings.llm.openai.model,
            temperature=0
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            google_api_key=settings.llm.gemini.api_key,
            model=settings.llm.gemini.model,
            temperature=0
        )
    elif provider == "ollama":
        return ChatOllama(
            base_url=settings.llm.ollama.base_url,
            model=settings.llm.ollama.model,
            temperature=0
        )
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def get_embeddings() -> Embeddings:
    """Returns the configured Embeddings model for Memory."""
    provider = settings.llm.active_provider

    if provider == "openai":
        return OpenAIEmbeddings(api_key=settings.llm.openai.api_key)
    elif provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            google_api_key=settings.llm.gemini.api_key,
            model="models/embedding-001"
        )
    elif provider == "ollama":
        return OllamaEmbeddings(
            base_url=settings.llm.ollama.base_url,
            model=settings.llm.ollama.model
        )
    else:
        # Fallback to OpenAI if unknown, or raise error
        raise ValueError(f"Unknown Embedding provider: {provider}")