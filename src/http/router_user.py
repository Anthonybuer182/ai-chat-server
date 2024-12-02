
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.http.base_response import BaseResponse
from src.model.user import Token
router = APIRouter()
@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),response_model=BaseResponse[Token]):
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
    return {
        "code": 200,
        "message": "Success",
        "data": {}
    }
@router.post("/register")
async def register():
    return {"status": "ok", "message": "RealChar is running smoothly!"}

