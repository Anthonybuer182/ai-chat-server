from fastapi import APIRouter


http_router = APIRouter()

@http_router.get("/status")
async def status():
    return {"status": "ok", "message": "RealChar is running smoothly!"}