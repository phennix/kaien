import uuid
import time
import chromadb

class MemoryModule:
    def __init__(self):
        # Connect to local ChromaDB
        self.client = chromadb.PersistentClient(path="./data/kaien_db")
        self.collection = self.client.get_or_create_collection("kaien_knowledge")

    def remember(self, text: str):
        """Stores text in the vector database."""
        doc_id = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[{"timestamp": time.time()}],
            ids=[doc_id]
        )
        return f"Stored in memory (ID: {doc_id})"

    def recall(self, query: str, n_results: int = 2):
        """Retrieves relevant context."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if not results['documents'][0]:
            return "No relevant memories found."
        return "\n".join(results['documents'][0])