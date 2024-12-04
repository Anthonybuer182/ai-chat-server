
from math import exp
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.http.base_response import BaseResponse,success_response,failure_response
from src.model.user import Register, Token
router = APIRouter()
@router.post("/token")
async def token(request: OAuth2PasswordRequestForm = Depends(),response_model=BaseResponse[Token]):
    # user = fake_users_db.get(form_data.username)
    # if not user or user["password"] != form_data.password:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid credentials",
    #     )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = jwt.encode(
    #     {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
    #     SECRET_KEY,
    #     algorithm=ALGORITHM,
    # )
    return success_response(data=Token(access_token=request.username, token_type=request.password,expires_in=200))
@router.post("/register")
async def register(request:Register,response_model=BaseResponse[Token]):
    token_response = await token(request=OAuth2PasswordRequestForm(username=request.username, password=request.password))

    return token_response

