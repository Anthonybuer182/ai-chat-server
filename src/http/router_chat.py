from fastapi import APIRouter
router = APIRouter()
@router.get("/get_recent_conversations")
async def get_recent_conversations():
    return {"status": "ok", "message": "RealChar is running smoothly!"}
@router.post("{session_id}")
async def status():
    return {"status": "ok", "message": "RealChar is running smoothly!"}
