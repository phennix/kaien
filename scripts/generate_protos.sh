#!/bin/bash
# scripts/generate_protos.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Create the output directory for the generated files
mkdir -p extensions/system_ext/generated

# Run the gRPC Python code generator
python3 -m grpc_tools.protoc \
  --proto_path=protos \
  --python_out=extensions/system_ext/generated \
  --grpc_python_out=extensions/system_ext/generated \
  protos/system.proto

# Create an __init__.py file to make it a package
touch extensions/system_ext/generated/__init__.py