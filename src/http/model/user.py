from typing import Optional
from pydantic import BaseModel

class UserRequest(BaseModel):
    id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    code: Optional[str]