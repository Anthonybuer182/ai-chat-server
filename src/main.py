
import asyncio
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.database.postgre.connection import init_db
from src.api.exceptions import setup_exception_handlers
from src.api.router_config import restful_router
from sqlalchemy.exc import SQLAlchemyError
from src.util.logger import get_logger
from src.ws.websocket_router import websocket_router,manager

app =FastAPI()
logger = get_logger(__name__)

setup_exception_handlers(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.on_event("startup")
async def startup():
    try:
        await init_db()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database connection failed")
    asyncio.create_task(manager.broadcast_message_worker())
    logger.info("WebSocket server started.")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutting down WebSocket server...")
    await manager.message_queue.join()
    logger.info("All messages have been processed.")

app.include_router(restful_router)
app.include_router(websocket_router)

