from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

# Import database functions and lifespan context manager
from server.database import lifespan_db_connection, init_db

# Define the base data directory for databases as requested
DB_PATH = "./data/kaien_db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Use the database lifespan context manager for initialization
    async with lifespan_db_connection(base_data_dir=DB_PATH):
        print("Server starting up...")
        yield
        print("Server shutting down...")

app = FastAPI(title="Kaien Server", version="0.1.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers,
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Kaien Server is running"}

@app.get("/")
async def root():
    return {"status": "Kaien Nexus Online"}
