from typing import Optional
from pydantic import BaseModel

class UserRequest(BaseModel):
    id: Optional[str] = None
    username: str
    password: str
    phone: Optional[str] = None
    email: Optional[str] = None
    code: Optional[str] = None