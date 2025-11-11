#!/bin/bash
# scripts/generate_protos.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the output directory
OUT_DIR="extensions/system_ext/generated"

## Clean up previous generated files to prevent conflicts
#rm -rf ${OUT_DIR}
#
## Create the output directory
#mkdir -p ${OUT_DIR}

# Run the gRPC Python code generator
# The key change is adding --py_out and --grpc_py_out to create a package structure
python -m grpc_tools.protoc \
  --proto_path=protos \
  --python_out=${OUT_DIR} \
  --grpc_python_out=${OUT_DIR} \
  protos/system.proto

# Create an __init__.py file to make it a package
touch ${OUT_DIR}/__init__.py