
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from src.database.postgre.model.user import UserDB, create_user, edit_user, get_user_by_id
from src.http.model.chat import ChatRequest
from src.http.model.user import UserRequest
from src.http.router_auth2 import  get_current_user
from src.http.model.base import success_response,failure_response
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgre.connection import get_db
from src.multi_models.llm.ai_chat import AsyncAIChat, SyncAIChat

router = APIRouter()

@router.post("/text")
async def text(request:ChatRequest,user:UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    # 获取角色的系统提示
    
    # 获取向量数据库的话题上下文
    # 获取会话的消息上下文
    ai = AsyncAIChat(model="qwen-turbo",system_prompt=request.system_prompt,messages_context="")
    text = await ai(request.user_prompt,stream=False)
    return success_response(data=text)
@router.post("/image")
async def image(request:UserRequest,db: AsyncSession = Depends(get_db)):
    return success_response(data="图像生成")
@router.get("/audio")
async def audio(current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="音频生成")
@router.get("/video")
async def video(current_user: UserDB = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    return success_response(data="视频生成")

