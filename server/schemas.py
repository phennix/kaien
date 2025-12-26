from pydantic import BaseModel
from typing import Optional, Any

class AgentRequest(BaseModel):
    query: str

class AgentResponse(BaseModel):
    status: str
    result: str
    details: Optional[Any] = None