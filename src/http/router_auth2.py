import os
from re import U
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from jwt.exceptions import ExpiredSignatureError, DecodeError
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from config import SECRET_KEY
from src.database.postgre.connection import get_db
from src.database.postgre.model.user import  UserDB, get_user_by_id,get_user_by_name,verify_password
from src.util.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

router = APIRouter()

@router.post("/token")
async def token(request: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_db)):
    user = await get_user_by_name(db,request.username)
    if not user or not verify_password(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token,expire=create_access_token(user=user)
    return {"access_token":access_token,"token_type":"bearer","expires_in":expire}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):
    user = verify_token(token)
    #内存查询用户会不会好点
    # user = get_user_by_id(db,user.id)
    return user

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 1800

def create_access_token(user: UserDB, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode={"sub": user.id,"username":user.username,"exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt,(expire - datetime.utcnow()).seconds

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        if  user_id is None or username is None :
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return UserDB (id=user_id, username=username)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Token is invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.info(f"Unexpected error: {e}")
        raise HTTPException(status_code=401, detail="Token has expired or is invalid")
        