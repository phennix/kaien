import sqlite3
from chromadb.config import Settings
from chromadb import Client, Collection
import config
import os

def init_sqlite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sessions (id INTEGER PRIMARY KEY, data TEXT)')
    conn.commit()
    conn.close()

def init_chroma_db(persist_path: str):
    db_config = config.database_config
    client = Client(Settings(
        chroma_api_impl=db_config['chroma_api_implementation'],
        persist_directory=persist_path,
        chroma_server_host='localhost' if db_config['type'] == 'remote' else None,
        chroma_server_http_port=8000 if db_config['type'] == 'remote' else None
    ))
    collection = client.get_or_create_collection(name='kaien-memory')
    return collection