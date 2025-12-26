# Shell Agent: Safe async subprocess wrapper
import asyncio
import subprocess
from typing import Optional

class ShellAgent:
    async def run_command(
        self, command: str, timeout: int = 30
    ) -> tuple[Optional[str], Optional[str]]:
        """Execute shell command with timeout"""
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
            return stdout.decode(), stderr.decode()
        except asyncio.TimeoutError:
            return None, "Command timed out"
        except Exception as e:
            return None, str(e)