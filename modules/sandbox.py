import docker
import os

class Sandbox:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            print(f"Warning: Docker not available - {e}")
            self.client = None

    def run_test(self, test_command):
        if not self.client:
            return "Error: Docker not available."
        
        try:
            current_dir = os.getcwd()
            volumes = {current_dir: {'bind': '/app', 'mode': 'ro'}}
            
            container = self.client.containers.run(
                image='python:3.10-slim',
                command=test_command,
                volumes=volumes,
                working_dir='/app',
                detach=False,
                remove=True
            )
            
            return (0, container.decode('utf-8'))
        except Exception as e:
            return (1, str(e))