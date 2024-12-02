
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.http.exceptions import setup_exception_handlers
from src.http.router_config import combined_router

app =FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(combined_router)
setup_exception_handlers(app)