from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str
    phone: str 
    email: str
    code: str 