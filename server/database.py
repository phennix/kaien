import sqlite3
from chromadb.config import Settings
from chromadb import Collection

# Initialize SQLite database
def init_sqlite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, data TEXT)')
    conn.commit()
    conn.close()

# Initialize ChromaDB vector store
def init_chroma_db(persist_directory: str):
    from chromadb import Client
    client = Client(Settings(chroma_api_impl='rest', chroma_server_host='localhost', chroma_server_http_port='8000'))
    collection = client.get_or_create_collection(name='kaien-memory')
    return collection