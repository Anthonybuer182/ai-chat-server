from typing import Optional
from pydantic import BaseModel

class UserRequest(BaseModel):
    id: Optional[str]
    username: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    code: Optional[str] = None