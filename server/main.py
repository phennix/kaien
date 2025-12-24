from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import database

db_path = 'kaien.db'
persist_directory = 'chroma_db'

database.init_sqlite_db(db_path)
collection = database.init_chroma_db(persist_directory)

app = FastAPI()

class SessionData(BaseModel):
    data: str

@app.get('/')
def read_root():
    return {'Hello': 'Kaien Server'}

@app.post('/session')
def create_session(session_data: SessionData):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sessions (data) VALUES (?)', (session_data.data,))
    conn.commit()
    conn.close()
    return {'message': 'Session created'}

@app.post('/memory')
def add_memory(memory_data: SessionData):
    collection.add(ids=['id1'], embeddings=[[1.0, 2.0]], metadatas=[{'source': 'user_input'}], documents=[memory_data.data])
    return {'message': 'Memory added'}