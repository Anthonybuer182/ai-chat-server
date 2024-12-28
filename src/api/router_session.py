from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.sql import get_db
from src.database.postgre.model.session import create_session, delete_session, edit_session, get_session_by_id, get_session_list
from src.database.postgre.model.user import UserDB
from src.api.model.base import success_response
from src.api.model.session import SessionListRequest, SessionRequest
from src.api.model.pagination import PaginationResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router_auth2 import get_user
router = APIRouter()

@router.post("/create")
async def create(request:SessionRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    session = await create_session(db=db,user=user,session=request)
    return success_response(data=jsonable_encoder(session))

@router.post("/delete/{id}")
async def delete(id:str,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    result = await delete_session(db=db,user_id=user.id,session_id=id)
    return success_response(data=result)

@router.post("/edit")
async def edit(request:SessionRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    session = await edit_session(db=db,user=user,session=request)
    return success_response(data=jsonable_encoder(session))

@router.get("/get/{id}")
async def get(id: str,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    session=await get_session_by_id(db,id)
    return success_response(data=jsonable_encoder(session))

@router.post("/list")
async def list(request:SessionListRequest,user: UserDB = Depends(get_user),db: AsyncSession = Depends(get_db)):
    sessions = await get_session_list(db=db,sessionList=request)
    return success_response(data=sessions)
