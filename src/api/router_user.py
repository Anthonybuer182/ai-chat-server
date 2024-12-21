
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.model.user import UserDB, create_user, delete_user, edit_user, get_user_by_id
from src.api.model.user import UserRequest
from src.api.router_auth2 import  get_user
from src.api.model.base import success_response,failure_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db

router = APIRouter()

@router.post("/register")
async def register(request:UserRequest,db: AsyncSession = Depends(get_db)):
    user=await create_user(db, user=request)
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

@router.post("/delete/{id}")
async def delete(id:str,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    result=await delete_user(db, user_id=id)
    return success_response(data=result)

@router.post("/edit")
async def edit(request:UserRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    user=await edit_user(db, user=request)
    if not user:
        return failure_response(message="user not found")
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

@router.get("/get")
async def get(user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    user=await get_user_by_id(db, user.id)
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

