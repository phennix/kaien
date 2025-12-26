import docker
import os

class Sandbox:
    def __init__(self):
        self.client = docker.from_env()
        self.image_name = "kaien-sandbox"

    def setup(self):
        # Build a Docker image based on python:3.10-slim
        dockerfile_content = """
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . .
"""
        # Write Dockerfile to a temporary location
        with open("Dockerfile.sandbox", "w") as f:
            f.write(dockerfile_content)

        # Build the image
        image, logs = self.client.images.build(path=".", dockerfile="Dockerfile.sandbox", tag=self.image_name)
        
        # Clean up temporary Dockerfile
        os.remove("Dockerfile.sandbox")
        
        return image, logs

    def run_test(self, test_command):
        # Ensure the image is built
        try:
            self.client.images.get(self.image_name)
        except docker.errors.ImageNotFound:
            self.setup()

        # Run the test in a container
        container = self.client.containers.run(
            self.image_name,
            command=test_command,
            volumes={os.getcwd(): {"bind": "/app", "mode": "ro"}},
            working_dir="/app",
            detach=True,
            stderr=True,
            stdout=True
        )

        # Wait for the container to finish and capture logs
        exit_code = container.wait()
        logs = container.logs().decode("utf-8")

        return exit_code, logs