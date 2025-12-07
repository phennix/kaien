# src/kaien/memory/db.py
import chromadb
import uuid
import os
import time
from kaien.config import settings
from kaien.agent.factory import get_embeddings


class MemoryEngine:
    def __init__(self):
        # Ensure data directory exists
        os.makedirs(settings.storage.data_dir, exist_ok=True)
        chroma_path = os.path.join(settings.storage.data_dir, "chroma_db")

        self.client = chromadb.PersistentClient(path=chroma_path)
        self.collection_name = settings.storage.memory_collection_name
        self.embeddings = get_embeddings()

    def _get_collection(self):
        # We use the embedding function wrapper for Chroma
        # Note: LangChain embeddings -> Chroma embedding function adapter might be needed
        # For simplicity in this phase, we embed manually before inserting
        return self.client.get_or_create_collection(name=self.collection_name)

    def add_interaction(self, user_input: str, agent_response: str):
        """Save a turn of conversation with embeddings."""
        text = f"User: {user_input}\nAgent: {agent_response}"

        # Generate embedding using LangChain wrapper
        vector = self.embeddings.embed_query(text)

        collection = self._get_collection()
        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[vector],
            metadatas=[{"timestamp": time.time(), "type": "conversation"}]
        )

    def search(self, query: str, n_results=3) -> list[str]:
        """Retrieve relevant context."""
        vector = self.embeddings.embed_query(query)

        collection = self._get_collection()
        results = collection.query(
            query_embeddings=[vector],
            n_results=n_results
        )

        if results and results['documents']:
            return results['documents'][0]  # Chroma returns list of lists
        return []