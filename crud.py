from fastapi import FastAPI , HTTPException
from sqlalchemy.orm import Session
from schemas import IpInfoResponse
from models import IpInfoApi

def create_api(db  : Session , apiappinfodate  : IpInfoResponse):
    db_apiappinfodat = IpInfoApi(ip =  apiappinfodate.ip , city =  apiappinfodate.city , region =  apiappinfodate.region ,counter =  apiappinfodate.counter ,
                              location =  apiappinfodate.location , org =  apiappinfodate.org , postal =  apiappinfodate.postal , 
                              timezone =  apiappinfodate.timezone 
                              )
    
    db.add(db_apiappinfodat)
    db.commit()
    db.refresh(db_apiappinfodat)

    return db_apiappinfodat


def get_apiinfo(db : Session , ipinfoapp_id : int):
    return db.query(IpInfoApi).filter(IpInfoApi.id==ipinfoapp_id).first()

def update_apiinfo(db  :Session , ipinfoapp_id : int , apiappinfodate  : IpInfoResponse):
    db_apiappinfodat = db.query(IpInfoApi).filter(IpInfoApi.id == ipinfoapp_id).first()

    if db_apiappinfodat is None:
        return None
    
    db_apiappinfodat.ip = apiappinfodate.ip
    db_apiappinfodat.city = apiappinfodate.city
    db_apiappinfodat.region = apiappinfodate.region
    db_apiappinfodat.counter = apiappinfodate.counter
    db_apiappinfodat.location = apiappinfodate.location
    db_apiappinfodat.org = apiappinfodate.org
    db_apiappinfodat.postal = apiappinfodate.postal
    db_apiappinfodat.timezone = apiappinfodate.timezone

    db.commit()
    db.refresh(db_apiappinfodat)

    return db_apiappinfodat

def delete_apiinfo(db  : Session , ipinfoapp_id : int):
    db_apiappinfodat = db.query(IpInfoApi).filter(IpInfoApi.id == ipinfoapp_id).first()

    if db_apiappinfodat is None:
        raise HTTPException(status_code=404 , detail="Apiappinfodata Deleted Successfully")
    

    db.delete(db_apiappinfodat)
    db.commit()
    db.refresh(db_apiappinfodat)
    return {"detail": "Employee Data Successfully Deleted"}



