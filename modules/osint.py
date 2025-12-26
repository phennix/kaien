"""OSINT Module - Safe shell command execution with timeouts"""

import subprocess
import asyncio
import logging

logger = logging.getLogger(__name__)

class OSINTModule:
    """OSINT operations with strict timeout enforcement"""
    
    def __init__(self):
        # Define allowed commands for OSINT operations
        self.allowed_commands = ["ping", "curl", "whois", "nslookup", "nmap", "ls", "grep"]
        self.timeout_seconds = 15  # Strict timeout for all commands
        logger.info("OSINT Module initialized with allowed commands: %s", self.allowed_commands)
    
    async def run_command(self, command: str):
        """
        Executes a shell command asynchronously with strict timeout.
        
        Security Note: Only allows specific OSINT-related commands.
        All commands are limited to 15 seconds execution time.
        """
        if not command or not isinstance(command, str):
            return "Error: Invalid command"
        
        # Extract base command
        cmd_parts = command.strip().split()
        if not cmd_parts:
            return "Error: Empty command"
        
        cmd_base = cmd_parts[0].split("/")[-1]  # Get just the command name
        
        # Security check - only allow specific commands
        if cmd_base not in self.allowed_commands:
            logger.warning(f"Blocked disallowed command: {cmd_base}")
            return f"Error: Command '{cmd_base}' is not in the allowed OSINT list."
        
        try:
            logger.info(f"Executing OSINT command: {command}")
            
            # Execute command
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for completion with strict timeout
            try:
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=self.timeout_seconds)
            except asyncio.TimeoutError:
                proc.kill()
                await proc.wait()
                logger.warning(f"Command timed out: {command}")
                return f"Error: Command timed out (limit {self.timeout_seconds}s)."
            
            # Process output
            output = stdout.decode().strip() if stdout else ""
            error = stderr.decode().strip() if stderr else ""
            
            if error:
                logger.warning(f"Command error: {error}")
                return f"Output:\n{output}\nErrors:\n{error}" if output else f"Errors:\n{error}"
            
            logger.info(f"Command completed successfully: {cmd_base}")
            return output if output else "Command executed successfully (no output)"
            
        except Exception as e:
            logger.error(f"OSINT command execution failed: {str(e)}")
            return f"Execution failed: {str(e)}"