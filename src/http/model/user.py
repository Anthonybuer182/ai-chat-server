from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str
    phone: str 
    email: str
    code: str 