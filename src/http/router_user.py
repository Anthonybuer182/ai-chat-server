
from math import exp
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from src.database.postgre.connection import get_db
from src.database.postgre.db_user import create_user, get_user,verify_password
from src.http import auth2
from src.http.base_response import BaseResponse,success_response,failure_response
from src.model.user import Register, Token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/token")
async def token(request: OAuth2PasswordRequestForm = Depends(),response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user = await get_user(db,request.username)
    if not user or not verify_password(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token,expire=auth2.create_access_token(data={"sub": request.username})
    return success_response(data=Token(access_token=access_token, token_type="bearer",expires_in=expire))
@router.post("/register")
async def register(request:Register,response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user=await create_user(db, request.username, request.password, request.phone, request.email)
    access_token,expire=auth2.create_access_token(data={"sub": user.username})
    return success_response(data=Token(access_token=access_token, token_type="bearer",expires_in=expire))

