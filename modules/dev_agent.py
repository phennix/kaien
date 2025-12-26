# Dev Agent: File manipulation and testing
import os
from pathlib import Path

class DevAgent:
    def read_file(self, path: str) -> str:
        """Read file content"""
        return Path(path).read_text()
    
    def write_file(self, path: str, content: str):
        """Write file content"""
        Path(path).write_text(content)
    
    def test_python(self, code: str) -> dict:
        """Test Python code execution"""
        try:
            exec(code)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}