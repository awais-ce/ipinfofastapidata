import grpc
import ipinfo_pb2
import ipinfo_pb2_grpc

def run_client():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ipinfo_pb2_grpc.IPInfoServiceStub(channel)
        ip = input("Enter the value of the IP Address: ")
        response = stub.SayIpInfo(ipinfo_pb2.IpRequest(ip=ip))
        print("IP information:")
        print(f"Ip: {response.ip}")
        print(f"City: {response.city}")
        print(f"Region: {response.region}")
        print(f"Country: {response.country}")
        print(f"Location: {response.location}")
        print(f"Org: {response.org}")
        print(f"Postal: {response.postal}")
        print(f"Timezone: {response.timezone}")

if __name__ == "__main__":
    run_client()


