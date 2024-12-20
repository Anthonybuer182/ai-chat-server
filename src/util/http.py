import os
import uuid
import httpx

from config import PROXY
from src.util.logger import get_logger

# 设置日志记录器
logger = get_logger(__name__)

def sync_client() -> httpx.Client:
    """创建同步客户端"""
    return httpx.Client(
        proxies=PROXY,
        timeout=60,
        event_hooks={
            "request": [log_request],
            "response": [log_response],
        }
    )

def async_client() -> httpx.AsyncClient:
    """创建异步客户端"""
    return httpx.AsyncClient(
        proxies=PROXY,
        timeout=60,
        event_hooks={
            "request": [async_log_request],
            "response": [async_log_response],
        }
    )

MAX_BODY_LENGTH = 50000  # 限制请求和响应体的最大长度

def log_request(request: httpx.Request):
    """同步请求日志"""
    request_id = add_request_id(request)
    body = ""
    if request.content:
        try:
            body = request.content.decode('utf-8')
            # 如果 body 中包含 Unicode 转义字符，进行解码
            body = bytes(body, 'utf-8').decode('unicode_escape')
        except Exception as e:
            logger.warning(f"Failed to decode request body: {e}")
    log_http_message(request_id, "HTTP REQUEST", request.method, str(request.url), request.headers, body)

def log_response(response: httpx.Response):
    """同步响应日志"""
    request_id = response.request.extensions.get('request_id', 'N/A')
    try:
        body = response.text or response.read().decode(response.encoding or 'utf-8')
    except Exception as e:
        logger.warning(f"Failed to read response body: {e}")
        body = "[Failed to read body]"
    log_http_message(request_id, "HTTP RESPONSE", response.request.method, str(response.request.url), response.headers, body)

async def async_log_request(request: httpx.Request):
    """异步请求日志"""
    request_id = add_request_id(request)
    body = ""
    if request.content:
        try:
            body = request.content.decode('utf-8')
            # 如果 body 中包含 Unicode 转义字符，进行解码
            body = bytes(body, 'utf-8').decode('unicode_escape')
        except Exception as e:
            logger.warning(f"Failed to decode request body: {e}")
    log_http_message(request_id, "HTTP REQUEST", request.method, str(request.url), request.headers, body)

async def async_log_response(response: httpx.Response):
    """异步响应日志"""
    request_id = response.request.extensions.get('request_id', 'N/A')
    try:
        if response.stream:
            content = await response.aread()
            body = content.decode(response.encoding or 'utf-8')
        else:
            body = response.text
    except Exception as e:
        logger.warning(f"Failed to read response body: {e}")
        body = "[Failed to read body]"
    log_http_message(request_id, "HTTP RESPONSE", response.request.method, str(response.request.url), response.headers, body)

def truncate_content(content: str) -> str:
    """截断内容，限制输出长度"""
    if len(content) > MAX_BODY_LENGTH:
        return f"{content[:MAX_BODY_LENGTH]}... [Content truncated, total length: {len(content)}]"
    return content

def add_request_id(request: httpx.Request) -> str:
    """为请求添加唯一标识符"""
    request_id = str(uuid.uuid4())
    request.extensions['request_id'] = request_id
    return request_id

def log_http_message(request_id: str, title: str, method: str, url: str, headers: dict, body: str):
    """统一的日志输出"""
    logger.info(f"====== {title} START ======")
    logger.info(f"Request ID: {request_id}")
    logger.info(f"Method: {method}")
    logger.info(f"URL: {url}")
    logger.info("Headers:")
    for k, v in headers.items():
        if k.lower() == "authorization":
            v = "[FILTERED]"
        logger.info(f"    {k}: {v}")
    logger.info(f"Body:\n{truncate_content(body) if body else '[No content]'}")
    logger.info(f"====== {title} END ======\n")