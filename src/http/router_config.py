from fastapi import FastAPI,APIRouter
from src.http import router_character, router_chat, router_user
combined_router = APIRouter()

combined_router.include_router(router_user.router, prefix="/user", tags=["User"])
combined_router.include_router(router_character.router, prefix="/character", tags=["Character"])
combined_router.include_router(router_chat.router, prefix="/chat", tags=["Chat"])
