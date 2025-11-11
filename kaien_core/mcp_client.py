# gRPC client for communicating with extensions

# kaien_core/mcp_client.py
import grpc
import sys
import os

# NOTE: You must run generate_protos.sh first
# from extensions.system_ext.generated import system_pb2, system_pb2_grpc

# This assumes you run the CLI from the root 'kaien' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
from extensions.system_ext.generated import system_pb2
from extensions.system_ext.generated import system_pb2_grpc


class MCPClient:
    def __init__(self, address: str):
        self.channel = grpc.insecure_channel(address)
        self.system_stub = system_pb2_grpc.SystemStub(self.channel)

    def ping_system(self) -> str:
        """Calls the Ping RPC on the system extension."""
        try:
            request = system_pb2.PingRequest()
            response = self.system_stub.Ping(request)
            return response.message
        except grpc.RpcError as e:
            return f"Error calling Ping: {e.details()}"