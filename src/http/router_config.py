from fastapi import APIRouter
from src.http import router_auth2, router_character, router_conversation, router_generate, router_user
combined_router = APIRouter()
combined_router.include_router(router_auth2.router, tags=["Token"])
combined_router.include_router(router_user.router, prefix="/user", tags=["User"])
combined_router.include_router(router_character.router, prefix="/character", tags=["Character"])
combined_router.include_router(router_conversation.router, prefix="/conversation", tags=["Conversation"])
combined_router.include_router(router_generate.router, prefix="/generate", tags=["Generate"])

