import asyncio

class ShellAgent:
    async def execute_command(self, command: str) -> dict:
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode == 0:
                return {"status": "success", "output": stdout.decode().strip(), "returncode": process.returncode}
            else:
                return {"status": "error", "output": stderr.decode().strip(), "returncode": process.returncode}
        except Exception as e:
            return {"status": "exception", "output": str(e), "returncode": -1}

# This agent will be integrated with the Server for tool dispatch.