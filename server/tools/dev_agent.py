import os
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

class FileOperation(BaseModel):
    path: str
    content: Optional[str] = None

class DevAgent:
    def __init__(self):
        self.base_dir = os.getcwd()
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to a file"""
        try:
            # Security check - prevent directory traversal
            if ".." in path or path.startswith("/"):
                return {
                    "success": False,
                    "error": "Invalid path - directory traversal not allowed"
                }
            
            # Create directories if needed
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            # Write file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            
            return {
                "success": True,
                "path": path,
                "bytes_written": len(content)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """Read content from a file"""
        try:
            # Security check
            if ".." in path or path.startswith("/"):
                return {
                    "success": False,
                    "error": "Invalid path - directory traversal not allowed"
                }
            
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"File not found: {path}"
                }
            
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return {
                "success": True,
                "path": path,
                "content": content,
                "size": len(content)
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    def list_files(self, path: str = ".") -> Dict[str, Any]:
        """List files in a directory"""
        try:
            # Security check
            if ".." in path or path.startswith("/"):
                return {
                    "success": False,
                    "error": "Invalid path - directory traversal not allowed"
                }
            
            full_path = os.path.join(self.base_dir, path)
            
            if not os.path.exists(full_path):
                return {
                    "success": False,
                    "error": f"Path not found: {path}"
                }
            
            if not os.path.isdir(full_path):
                return {
                    "success": False,
                    "error": f"Not a directory: {path}"
                }
            
            files = []
            dirs = []
            
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                if os.path.isdir(item_path):
                    dirs.append(item)
                else:
                    files.append(item)
            
            return {
                "success": True,
                "path": path,
                "directories": dirs,
                "files": files
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": path
            }
    
    def test_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Test code execution"""
        try:
            if language == "python":
                # Simple syntax check
                compile(code, "<string>", "exec")
                return {
                    "success": True,
                    "message": "Python syntax is valid"
                }
            else:
                return {
                    "success": False,
                    "error": f"Language {language} not supported for testing"
                }
        
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax error: {str(e)}",
                "line": e.lineno,
                "offset": e.offset
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance
dev_agent = DevAgent()