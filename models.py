from sqlalchemy import String, Integer , Column
from sqlalchemy.ext.declarative import declarative_base
from database import *
Base = declarative_base()

class IpInfoApi(Base):
    __tablename__ = 'apiappinfodate' 

    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String)
    city = Column(String)
    region = Column(String)
    counter = Column(String)
    location = Column(String)
    org = Column(String)
    postal = Column(String)
    timezone = Column(String)
    
    

