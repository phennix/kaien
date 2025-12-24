from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
import chromadb
import os

# Global variables for database engine and session (SQLite)
async_engine = None
AsyncSessionLocal = None

Base = declarative_base()

async def init_sqlite_tables(base_dir: str):
    """Initializes the SQLite database tables and sets up the engine/session factory.
    The database file will be created inside the given base_dir."""
    global async_engine, AsyncSessionLocal
    
    sqlite_db_file = os.path.join(base_dir, "kaien_sessions.db")
    sqlite_url = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{sqlite_db_file}")

    # Ensure the directory for the SQLite database file exists
    os.makedirs(os.path.dirname(sqlite_db_file), exist_ok=True)

    async_engine = create_async_engine(sqlite_url, echo=False) # Set echo=True for SQL logging
    AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"SQLite tables created/checked at {sqlite_db_file}.")

async def get_async_session():
    """Dependency to get an async database session."""
    if AsyncSessionLocal is None:
        raise Exception("SQLite SessionLocal not initialized. Call init_sqlite_tables first.")
    async with AsyncSessionLocal() as session:
        yield session

# --- ChromaDB for Vector Memory ---
_vector_db_client = None

def init_db(path: str):
    """Initializes the ChromaDB client with a persistent path."""
    global _vector_db_client
    if _vector_db_client is None:
        os.makedirs(path, exist_ok=True)
        _vector_db_client = chromadb.PersistentClient(path=path)
        print(f"ChromaDB client initialized at {path}")
    return _vector_db_client

def get_chroma_client():
    """Returns the global ChromaDB client instance."""
    if _vector_db_client is None:
        raise Exception("ChromaDB client not initialized. Call init_db first (e.g., via lifespan_db_connection).")
    return _vector_db_client

@asynccontextmanager
async def lifespan_db_connection(base_data_dir: str):
    """
    Context manager for database connections during application lifespan.
    Initializes both SQLite and ChromaDB during startup within the specified base_data_dir.
    """
    print(f"Initializing database connections in {base_data_dir}...")
    
    # Ensure the base data directory exists
    os.makedirs(base_data_dir, exist_ok=True)

    # Initialize SQLite (path configured internally via env var or default)
    await init_sqlite_tables(base_data_dir)

    # Initialize ChromaDB using the new init_db function
    chroma_path = os.path.join(base_data_dir, "kaien_vector_db")
    init_db(chroma_path)

    yield

    print("Database connections shut down.")
