from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# --- Database Imports ---
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
# import chromadb

# Placeholder for database engine and session
# async_engine = None
# AsyncSessionLocal = None
# vector_db_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Server starting up...")
    
    # Initialize SQLite for session history
    # global async_engine, AsyncSessionLocal
    # async_engine = create_async_engine("sqlite+aiosqlite:///./kaien_sessions.db", echo=True)
    # AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    # await init_db() # Function to create tables

    # Initialize ChromaDB for vector memory
    # global vector_db_client
    # vector_db_client = chromadb.PersistentClient(path="./kaien_vector_db")
    # print("ChromaDB client initialized.")

    yield

    # Shutdown
    print("Server shutting down...")
    # Close database connections if necessary

app = FastAPI(title="Kaien Server", version="0.1.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Kaien Server is running"}

@app.get("/")
async def root():
    return {"status": "Kaien Nexus Online"}

# Placeholder for database initialization function (e.g., creating tables)
# async def init_db():
#     async with async_engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.create_all) # Base would be imported from a models file
#         pass
