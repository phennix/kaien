"""Agent Client - Communication layer for Kaien agents"""

import httpx
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)


class AgentRequest(BaseModel):
    """Request model for agent communication"""
    query: str
    session_id: Optional[str] = None
    metadata: Optional[Dict] = None


class AgentResponse(BaseModel):
    """Response model for agent communication"""
    status: str
    result: Any
    error: Optional[str] = None
    metadata: Optional[Dict] = None


class AgentClient:
    """Client for communicating with Kaien agents"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def send_request(self, agent_name: str, request: AgentRequest) -> AgentResponse:
        """Send request to a specific agent"""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/agent/{agent_name}",
                json=request.dict()
            )
            response.raise_for_status()
            
            data = response.json()
            return AgentResponse(**data)
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Agent {agent_name} request failed: {str(e)}")
            return AgentResponse(
                status="error",
                result=None,
                error=str(e),
                metadata={"agent": agent_name}
            )
        
        except Exception as e:
            logger.error(f"Error communicating with agent {agent_name}: {str(e)}")
            return AgentResponse(
                status="error",
                result=None,
                error=str(e),
                metadata={"agent": agent_name}
            )
    
    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/agent/{agent_name}/status")
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            logger.error(f"Error getting status for agent {agent_name}: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def list_agents(self) -> Dict[str, Any]:
        """List available agents"""
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/agents")
            response.raise_for_status()
            return response.json()
        
        except Exception as e:
            logger.error(f"Error listing agents: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
agent_client = AgentClient()