# The gRPC server implementation

# extensions/system_ext/server.py
import grpc
import time
from concurrent import futures

# Import generated classes
# NOTE: You must run generate_protos.sh first
from extensions.system_ext.generated import system_pb2, system_pb2_grpc


# Service implementation
class SystemService(system_pb2_grpc.SystemServicer):
    def Ping(self, request, context):
        print("Received Ping request.")
        return system_pb2.PingResponse(message="pong")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    system_pb2_grpc.add_SystemServicer_to_server(SystemService(), server)
    server.add_insecure_port('[::]:50051')
    print("System Extension Server started on port 50051.")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()