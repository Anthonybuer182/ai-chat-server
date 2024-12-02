from fastapi import APIRouter
router = APIRouter()
@router.get("/create_character/{character_id}")
async def create_character():
    return {"status": "ok", "message": "RealChar is running smoothly!"}
@router.get("/get_character/{character_id}")
async def get_character():
    return {"status": "ok", "message": "RealChar is running smoothly!"}
