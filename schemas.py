from pydantic import BaseModel, EmailStr


class IpInfoResponse(BaseModel):
    ip : str
    city : str
    region : str
    counter : str
    location : str
    org : str
    postal : str
    timezone : str


