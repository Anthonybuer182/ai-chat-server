from logging import getLogger
import os
import httpx



# 设置日志记录器
logger = getLogger(__name__)

def log_request(request: httpx.Request):
    logger.info("------ Request ------")
    # logger.info(f"Request: {request.method} {request.url}")
    # logger.info(f"Request headers: {request.headers}")
    if request.content:
        logger.info(f"Request body: {request.content.decode().encode('utf-8').decode('unicode_escape')}")
    else:
        logger.info("Request body: No content")

def log_response(response: httpx.Response):
    logger.info("------ Response ------")
    logger.info(f"Response {response.request.method} {response.request.url} - {response.status_code}")
    # logger.info(f"Response headers: {response.headers}")
    if response.stream:
        content = response.read()
    else:
        content = response.text
    body = content.decode(response.encoding or 'utf-8')
    logger.info(f"Response body: {body}")

async def async_log_request(request: httpx.Request):
    logger.info("------ Request ------")
    if request.content:
        logger.info(f"Request body: {request.content.decode().encode('utf-8').decode('unicode_escape')}")
    else:
        logger.info("Request body: No content")

async def async_log_response(response: httpx.Response):
    logger.info("------ Response ------")
    logger.info(f"Response {response.request.method} {response.request.url} - {response.status_code}")
    if response.stream:
        content = await response.aread()  # 注意这里需要 `await`
    else:
        content = response.text
    body = content.decode(response.encoding or 'utf-8')
    logger.info(f"Response body: {body}")

def sync_client(proxy: bool = True) -> httpx.Client:
    proxies = os.getenv("https_proxy") if proxy else None
    return httpx.Client(
        proxies=proxies,
        timeout=60,
        event_hooks={
            "request": [log_request],
            "response": [log_response],
        }
    )
def async_client(proxy: bool = True) -> httpx.AsyncClient:
    proxies = os.getenv("https_proxy") if proxy else None
    return httpx.AsyncClient(
        proxies=proxies,
        timeout=60,
        event_hooks={
            "request": [async_log_request],
            "response": [async_log_response],
    })
