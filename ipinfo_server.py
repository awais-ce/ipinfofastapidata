import grpc
import ipinfo_pb2
import ipinfo_pb2_grpc
from concurrent import futures
import requests

API_TOKEN = "091f71fa3f0840"

class IPInfoServiceServicer(ipinfo_pb2_grpc.IPInfoServiceServicer):

    def SayIpInfo(self, request, context):
        ip = request.ip
        response = requests.get(f"https://ipinfo.io/{ip}?token={API_TOKEN}")

        if response.status_code != 200:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("IP information Not Found")
            return ipinfo_pb2.IpReply()
        
        data = response.json()

        return ipinfo_pb2.IpReply(
            ip=data.get("ip", ip),
            city=data.get("city", "Unknown"),
            region=data.get("region", "Unknown"),
            country=data.get("country", "Unknown"),
            location=data.get("loc", "Unknown"),
            org=data.get("org", "Unknown"),
            postal=data.get("postal", "Unknown"),
            timezone=data.get("timezone", "Unknown"),
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ipinfo_pb2_grpc.add_IPInfoServiceServicer_to_server(IPInfoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()



