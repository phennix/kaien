from server.database.vector_db import VectorDB
from server.database.session_db import save_session_data, get_all_sessions
from typing import List, Dict, Any
import uuid

class MemoryManager:
    def __init__(self):
        self.vector_db = VectorDB()

    def add_text_to_memory(self, text: str, metadata: Dict[str, Any] = None) -> str:
        doc_id = str(uuid.uuid4())
        if metadata is None:
            metadata = {}
        # Add a timestamp or other useful info if not present
        if 'timestamp' not in metadata:
            import datetime
            metadata['timestamp'] = datetime.datetime.now().isoformat()

        self.vector_db.add_documents(documents=[text], metadatas=[metadata], ids=[doc_id])
        return doc_id

    def retrieve_relevant_memory(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        results = self.vector_db.query_documents(query_texts=[query], n_results=n_results)
        # ChromaDB results format is a dictionary with 'ids', 'distances', 'metadatas', 'documents'
        # We want to return a list of dicts, each containing 'id', 'document', 'metadata', 'distance'
        formatted_results = []
        if results and results['ids']:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })
        return formatted_results

    def save_session_exchange(self, user_input: str, agent_output: str):
        save_session_data(user_input, agent_output)

    def get_session_history(self) -> List[tuple]:
        return get_all_sessions()

    def count_vector_memory(self) -> int:
        return self.vector_db.count()

# Example usage (can be removed or moved to tests later)
if __name__ == "__main__":
    try:
        manager = MemoryManager()

        # Add some memories
        manager.add_text_to_memory("The user asked to create a FastAPI server.", {"source": "system_log"})
        manager.add_text_to_memory("Agent successfully wrote 'server/main.py'.", {"source": "agent_action"})
        manager.add_text_to_memory("Kaien system focuses on modularity and autonomy.", {"source": "architecture"})

        print(f"Total items in vector memory: {manager.count_vector_memory()}")

        # Retrieve memories
        query_results = manager.retrieve_relevant_memory("What is Kaien about?")
        print("\nRelevant memories for 'What is Kaien about?':")
        for res in query_results:
            print(f"  - [Distance: {res['distance']:.2f}] {res['document']} (Source: {res['metadata'].get('source', 'N/A')})")

        # Save and retrieve session history
        manager.save_session_exchange("Tell me about the Kaien project.", "Kaien is an autonomous AI system with self-development capabilities.")
        manager.save_session_exchange("What are its core components?", "Server, Client, and Modules.")

        print("\nSession History:")
        for session in manager.get_session_history():
            print(f"  - ID: {session[0]}, Time: {session[1]}, Input: {session[2]}, Output: {session[3]}")

    except Exception as e:
        print(f"An error occurred during MemoryManager example execution: {e}")
        print("Please ensure 'chromadb' and 'sentence-transformers' (if using local embeddings) are installed.")
