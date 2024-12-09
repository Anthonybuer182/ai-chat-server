from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None
def success_response(data: T, message: str = "Success", code: int = 200) -> BaseResponse[T]:
    return BaseResponse(code=code, message=message, data=data)

def failure_response(message: str, code: int = 400) -> BaseResponse[None]:
    return BaseResponse(code=code, message=message, data=None)