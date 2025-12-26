import os
import ast
from modules.brain import Brain

class DeveloperAgent:
    def __init__(self):
        self.brain = Brain()

    def list_files(self, path=""):
        if not path:
            path = "."
        file_list = []
        for root, dirs, files in os.walk(path):
            # Respect .gitignore by skipping common directories
            dirs[:] = [d for d in dirs if d not in [".git", "__pycache__", "node_modules"]]
            for file in files:
                file_list.append(os.path.join(root, file))
        return file_list

    def read_code(self, file_path):
        with open(file_path, "r") as file:
            return file.read()

    def propose_change(self, goal):
        # Use the brain to generate a plan or diff
        prompt = f"Analyze the codebase and propose changes to achieve the following goal:\n{goal}"
        response = self.brain.think(prompt)
        return response

    def apply_change(self, file_path, new_content):
        # This function should only be called after human confirmation
        with open(file_path, "w") as file:
            file.write(new_content)
        return f"Applied changes to {file_path}"