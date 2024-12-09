
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.model.user import UserDB, create_user, get_user_by_id
from src.http.model.user import UserRequest
from src.http.router_auth2 import  get_current_user
from src.http.model.base import success_response,failure_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db

router = APIRouter()

@router.post("/register")
async def register(request:UserRequest,db: AsyncSession = Depends(get_db)):
    user=await create_user(db, request.username, request.password, request.phone, request.email)
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

@router.get("/get")
async def get_user(current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    user=await get_user_by_id(db, current_user.id)
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

