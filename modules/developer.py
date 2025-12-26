import os

class DeveloperAgent:
    def list_files(self, path=""):
        if not path:
            path = "."
        
        ignore_dirs = {'.git', '__pycache__', 'venv', 'env', 'node_modules'}
        
        result = []
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 2 * level
            result.append(f"{indent}{os.path.basename(root)}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                result.append(f"{subindent}{file}")
        
        return "\n".join(result)
    
    def read_file(self, path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def apply_change_preview(self, path, new_content):
        try:
            with open(path, 'r') as file:
                old_content = file.read()
            
            diff = []
            old_lines = old_content.splitlines()
            new_lines = new_content.splitlines()
            
            max_len = max(len(old_lines), len(new_lines))
            
            for i in range(max_len):
                old_line = old_lines[i] if i < len(old_lines) else ""
                new_line = new_lines[i] if i < len(new_lines) else ""
                
                if old_line != new_line:
                    if old_line:
                        diff.append(f"- {old_line}")
                    if new_line:
                        diff.append(f"+ {new_line}")
            
            return "\n".join(diff)
        except Exception as e:
            return f"Error generating preview: {e}"