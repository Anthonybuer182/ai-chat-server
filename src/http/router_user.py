
from math import exp
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from src.database.postgre.connection import get_db
from src.database.postgre.db_user import create_user, get_user
from src.http import auth2
from src.http.base_response import BaseResponse,success_response,failure_response
from src.model.user import Register, Token
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/token")
async def token(request: OAuth2PasswordRequestForm = Depends(),response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user = get_user(db,request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    auth2.create_access_token({"sub": request.username})
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = jwt.encode(
    #     {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
    #     SECRET_KEY,
    #     algorithm=ALGORITHM,
    # )
    return success_response(data=Token(access_token=request.username, token_type=request.password,expires_in=200))
@router.post("/register")
async def register(request:Register,response_model=BaseResponse[Token],db: AsyncSession = Depends(get_db)):
    user=create_user(db, request.username, request.password, request.phone, request.email)
    token_response = await token(request=OAuth2PasswordRequestForm(username=request.username, password=request.password))
    return token_response

