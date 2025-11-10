# gRPC client for communicating with extensions

# kaien_core/mcp_client.py
import grpc
# NOTE: You must run generate_protos.sh first
from extensions.system_ext.generated import system_pb2, system_pb2_grpc


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