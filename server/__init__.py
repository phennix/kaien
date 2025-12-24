# Server initialization and configuration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.config.settings import shared_settings
from shared.utils.logger import default_logger

app = FastAPI(title=shared_settings.app_name, debug=shared_settings.debug)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origents=["*"] if app.debug else ["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and vector store
from server.database import init_db
init_db()

# Initialize tools
from server.tools import tool_router
app.include_router(tool_router, prefix=shared_settings.api_prefix)

# Log server startup
default_logger.info(f"Server started in {app.debug} mode on {shared_settings.host}:{shared_settings.port}")
