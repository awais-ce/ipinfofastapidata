from fastapi import FastAPI , HTTPException , Query ,Depends
from schemas import IpInfoResponse
import grpc
import ipinfo_pb2
import ipinfo_pb2_grpc
from models import *
from sqlalchemy.orm import Session
from database import *
from crud import *
from database import engine

 
app = FastAPI()



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind = engine)
async def get_ip_info(ip: str) -> str:
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = ipinfo_pb2_grpc.IPInfoServiceStub(channel)
            response = stub.SayIpInfo(ipinfo_pb2.IpRequest(ip=ip))
            return IpInfoResponse(
                ip=response.ip,
                city=response.city,
                region=response.region,
                counter=response.counter,
                location=response.location,
                org=response.org,
                postal=response.postal,
                timezone=response.timezone
            )
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
        return "gRPC call failed"


@app.post("/apiappinfodate/create")
async def create_ip_info(apiappinfodate : IpInfoResponse , db  : Session = Depends(get_db)):

    db_apiappinfodat = create_api(db , apiappinfodate)

    grpc_response = await get_ip_info(apiappinfodate.ip)

    return {"grpc_response" :  grpc_response, "apiappinfodate" : db_apiappinfodat}

@app.get("/apiappinfodate/{ipinfoapp_id}")
async def get_apiinfo_api(ipinfoapp_id : int , db  : Session = Depends(get_db)):
    db_apiappinfodat = get_apiinfo(db , ipinfoapp_id)

    if db_apiappinfodat is None:
        raise HTTPException(status_code=404 , detail="Apipinfodata does not Found")
    
    grpc_response = await get_ip_info("12.34.178.94")
    return {"grpc_response" :  grpc_response, "apiappinfodate" : db_apiappinfodat}

@app.post("/apiappinfodate/update/{ipinfoapp_id}")
async def update_apiinfo_api(ipinfoapp_id : int , apiappinfodate : IpInfoResponse , db  : Session = Depends(get_db)):
    db_apiappinfodat = update_apiinfo(db , ipinfoapp_id , apiappinfodate)

    if db_apiappinfodat is None:
        raise HTTPException(status_code=404 , detail="Apinfodata does not Found")
    
    grpc_response = await get_ip_info(apiappinfodate.ip)

    return {"db_apiappinfodat" : db_apiappinfodat , "apiappinfodate" : grpc_response}


@app.post("/apiappinfodate/delete/{ipinfoapp_id}")
async def delete_apiinfo_api(ipinfoapp_id : int , db  : Session = Depends(get_db)):
    db_apiappinfodat = delete_apiinfo(db , ipinfoapp_id)

    if db_apiappinfodat is None:
        raise HTTPException(status_code=404 , detail="Apiappinfodata Does Not Found")
    

    grpc_response = await get_ip_info("12.34.178.94")

    return {"db_apiappinfodat" : db_apiappinfodat , "apiappinfodate" : grpc_response}



