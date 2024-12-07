
from math import exp
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from src.database.postgre.db_user import User, create_user, get_user_by_id,get_user_by_name,verify_password
from src.http.auth2 import create_access_token, get_current_user
from src.http.base_response import BaseResponse,success_response,failure_response
from src.model.user import Register, Token
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db

router = APIRouter()

@router.post("/token")
async def token(request: OAuth2PasswordRequestForm = Depends(),response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user = await get_user_by_name(db,request.username)
    if not user or not verify_password(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token,expire=create_access_token(data={"sub": user.id,"username":user.username})
    return success_response(data=Token(access_token=access_token, token_type="bearer",expires_in=expire))

@router.post("/register")
async def register(request:Register,db: AsyncSession = Depends(get_db),response_model=BaseResponse[Token]):
    user=await create_user(db, request.username, request.password, request.phone, request.email)
    access_token,expire=create_access_token(data={"sub": user.id,"username":user.username})
    return success_response(data=Token(access_token=access_token, token_type="bearer",expires_in=expire))

@router.get("/get")
async def get_user(current_user: User = Depends(get_current_user),response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user=await get_user_by_id(db, current_user.id)
    return success_response(data=jsonable_encoder(user, exclude={"password"}))

