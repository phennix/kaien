import chromadb
from chromadb.utils import embedding_functions
import os

# Assuming an OpenAI-compatible embedding function for demonstration.
# In a real scenario, this would be configured via LiteLLM or similar.
# For local testing, you might use SentenceTransformersEmbeddingFunction or a local LLM.

# It's better to make the embedding function configurable or use LiteLLM's integration.
# For now, let's use a placeholder that would require an API key if used with OpenAI directly.
# A more robust solution would abstract this via LiteLLM.

# Placeholder for a real embedding function. 
# For a true local-only setup without an external API, you'd use a local model.
# Example with Sentence Transformers (requires `sentence-transformers` package):
# from chromadb.utils import embedding_functions
# openai_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def get_embedding_function():
    # This should ideally come from LiteLLM configuration.
    # For a minimal local setup without API keys, you could use:
    try:
        from chromadb.utils import embedding_functions
        # This requires `openai` package and OPENAI_API_KEY environment variable
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )
    except Exception as e:
        print(f"Warning: Could not initialize OpenAIEmbeddingFunction. Error: {e}")
        print("Falling back to SentenceTransformer (all-MiniLM-L6-v2) for local embeddings.")
        print("Please ensure 'sentence-transformers' is installed if you wish to use it.")
        try:
            return embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        except Exception as se:
            print(f"Error initializing SentenceTransformer: {se}")
            print("Vector database will not be fully functional without an embedding function.")
            return None # Or raise an error, depending on desired strictness

class VectorDB:
    def __init__(self, collection_name="kaien_memory"):
        self.client = chromadb.PersistentClient(path="./kaien_vector_db")
        self.embedding_function = get_embedding_function()
        if self.embedding_function is None:
            raise ValueError("No suitable embedding function could be initialized for ChromaDB.")
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def query_documents(self, query_texts: list[str], n_results: int = 5):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results

    def get_document_by_id(self, doc_id: str):
        return self.collection.get(ids=[doc_id])

    def delete_document_by_id(self, doc_id: str):
        self.collection.delete(ids=[doc_id])

    def count(self):
        return self.collection.count()
