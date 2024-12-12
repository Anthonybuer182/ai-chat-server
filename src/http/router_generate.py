
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.model.user import UserDB, create_user, edit_user, get_user_by_id
from src.http.model.user import UserRequest
from src.http.router_auth2 import  get_current_user
from src.http.model.base import success_response,failure_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db

router = APIRouter()

@router.post("/text")
async def text(request:UserRequest,db: AsyncSession = Depends(get_db)):
    return success_response(data="文本生成")
@router.post("/image")
async def image(request:UserRequest,db: AsyncSession = Depends(get_db)):
    return success_response(data="图像生成")
@router.get("/audio")
async def get_user(current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="音频生成")
@router.get("/video")
async def get_user(current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="视频生成")

