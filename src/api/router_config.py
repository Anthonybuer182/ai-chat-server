from fastapi import APIRouter
from src.api import router_auth2, router_character, router_session, router_message, router_generate, router_user
restful_router = APIRouter()
restful_router.include_router(router_auth2.router, tags=["Token"])
restful_router.include_router(router_user.router, prefix="/user", tags=["User"])
restful_router.include_router(router_character.router, prefix="/character", tags=["Character"])
restful_router.include_router(router_session.router, prefix="/session", tags=["Session"])
restful_router.include_router(router_generate.router, prefix="/generate", tags=["Generate"])
restful_router.include_router(router_message.router, prefix="/message", tags=["Message"])

