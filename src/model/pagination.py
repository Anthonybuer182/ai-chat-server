from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginationRequest(BaseModel):
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")

class PaginationResponse(BaseModel, Generic[T]):
    total: int = Field(description="总数据量")
    total_pages: int = Field(description="总页数")
    current_page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    records: List[T]