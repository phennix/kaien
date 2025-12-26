# Dependency Injection for FastAPI
from fastapi import Depends
from .database import SessionDB

def get_db():
    db = SessionDB()
    try:
        yield db
    finally:
        db.conn.close()