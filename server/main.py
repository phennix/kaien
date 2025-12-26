import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import sys
from contextlib import asynccontextmanager

# --- MAGIC IMPORT FIX ---
# Allow importing from parent directory (to see 'modules')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Relative imports within 'server/' package
from database import init_db
from schemas import AgentRequest, AgentResponse

# Import from sibling 'modules/' package
try:
    from modules.mcp_client import MCPClient
except ImportError:
    # Fallback if running from root
    from core.modules.mcp_client import MCPClient

# Global State
mcp = None
db_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global mcp, db_client
    logger.info("--- KAIEN SYSTEM STARTUP ---")
    try:
        db_client = init_db("./data/kaien_db")
        logger.info("Database initialized")
        
        mcp = MCPClient()
        logger.info("MCP Client initialized")
        
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("--- KAIEN SYSTEM SHUTDOWN ---")

app = FastAPI(lifespan=lifespan)

# CORS - Allow Client (Port 5000) to talk to Server (Port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Kaien Nexus Online", "sessions": 0}

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "db": "connected" if db_client else "error",
        "mcp": "initialized" if mcp else "error"
    }

@app.post("/chat", response_model=AgentResponse)
async def chat_endpoint(request: AgentRequest):
    if not mcp:
        raise HTTPException(status_code=500, detail="MCP Agent not initialized")
    
    try:
        response_text = await mcp.process_query(request.query)
        return AgentResponse(
            status="success",
            result=response_text
        )
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)