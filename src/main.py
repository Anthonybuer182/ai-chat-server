
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from router import http_router

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
app.include_router(http_router)