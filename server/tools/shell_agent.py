"""Shell Agent - Safe async wrapper around subprocess"""

import asyncio
import subprocess
from typing import Dict, Any
from pydantic import BaseModel
import os
from ..config import config
import logging

logger = logging.getLogger(__name__)


class ShellCommand(BaseModel):
    command: str
    timeout: int = 60
    cwd: str = None


class ShellAgent:
    def __init__(self):
        self.safe_commands = config.get("safe_commands", ["ls", "mkdir", "cd", "pwd", "echo", "cat", "grep", "find"])
    
    async def execute(self, command: str, timeout: int = 60, cwd: str = None) -> Dict[str, Any]:
        """Execute a shell command safely"""
        
        logger.info(f"Executing shell command: {command}")
        
        # Security check
        if not self._is_safe_command(command):
            logger.warning(f"Blocked unsafe command: {command}")
            return {
                "success": False,
                "error": "Command not allowed",
                "command": command
            }
        
        try:
            # Run the command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd or os.getcwd()
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                logger.warning(f"Command timed out: {command}")
                return {
                    "success": False,
                    "error": "Command timed out",
                    "command": command
                }
            
            result = {
                "success": True,
                "command": command,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "returncode": process.returncode
            }
            
            logger.info(f"Command completed: {command} (exit code: {process.returncode})")
            return result
        
        except Exception as e:
            logger.error(f"Error executing command {command}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def _is_safe_command(self, command: str) -> bool:
        """Check if command is safe to execute"""
        # Check if command starts with safe commands
        cmd_parts = command.split()
        if not cmd_parts:
            return False
        
        base_cmd = cmd_parts[0].split("/")[-1]  # Get just the command name
        
        # Allow safe commands
        if base_cmd in self.safe_commands:
            return True
        
        # Check for dangerous patterns
        dangerous_patterns = [";", "&&", "|", ">", "<", "rm", "del", "mv", "cp"]
        for pattern in dangerous_patterns:
            if pattern in command:
                return False
        
        return False


# Singleton instance
shell_agent = ShellAgent()