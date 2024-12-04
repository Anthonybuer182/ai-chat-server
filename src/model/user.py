from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
class Register(BaseModel):
    username: str
    password: str
    phone: str 
    code: str 