
from fastapi import FastAPI

from src.router.http_router import router


app =FastAPI()
from fastapi.middleware.cors import CORSMiddleware
# 允许跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)