import os
import chromadb

def init_db(persist_path: str):
    """Initialize the local ChromaDB persistent client."""
    if not os.path.exists(persist_path):
        os.makedirs(persist_path, exist_ok=True)
    
    # Use PersistentClient for local storage
    client = chromadb.PersistentClient(path=persist_path)
    return client