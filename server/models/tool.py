from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

class ToolParameter(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    required: bool = False
    default: Optional[Any] = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: List[ToolParameter] = Field(default_factory=list)
    code: Optional[str] = None # For dynamic tools, the actual execution code

class ToolCall(BaseModel):
    tool_name: str
    args: Dict[str, Any]
