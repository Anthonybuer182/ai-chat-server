
from fastapi import APIRouter
from src.http.base_response import BaseResponse
router = APIRouter()

@router.post("/login",response_model=BaseResponse[List[Item]])
async def login():
    return {"status": "ok", "message": "RealChar is running smoothly!"}
@router.post("/register")
async def register():
    return {"status": "ok", "message": "RealChar is running smoothly!"}

