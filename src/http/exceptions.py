import traceback
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
async def internal_server_error_handler(request: Request, exc: Exception):
    error_message = str(exc) if exc else "内部服务器错误"
    error_details = {
        "code": 500,
        "message": error_message,
        "data": None,
    }
    return JSONResponse(
        status_code=500,
        content=error_details,
    )
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"code": 422, "message": "Validation Error", "data": exc.errors()},
    )
def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, internal_server_error_handler)