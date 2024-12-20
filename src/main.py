
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.database.postgre.connection import init_db
from src.http.exceptions import setup_exception_handlers
from src.http.router_config import restful_router
from sqlalchemy.exc import SQLAlchemyError
app =FastAPI()
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
    
app.include_router(restful_router)
app.include_router(restful_router)
