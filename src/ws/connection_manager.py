from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
from datetime import datetime
from dataclasses import dataclass, asdict

from fastapi.websockets import WebSocketState

from src.util.logger import get_logger

logger = get_logger(__name__)
class ConnectionManager:
    def __init__(self):
        # 存储所有活跃连接
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # 消息队列
        self.message_queue: asyncio.Queue = asyncio.Queue()
        # 连接计数器
        self.connection_counter = 0
        # 锁,用于保护共享资源
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, session_id: str):
        try:
            await websocket.accept()
            async with self.lock:
                if session_id not in self.active_connections:
                    self.active_connections[session_id] = set()
                self.active_connections[session_id].add(websocket)
                self.connection_counter += 1
                logger.info(f"New connection in session {session_id}. Total connections: {self.connection_counter}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")

    async def disconnect(self, websocket: WebSocket, session_id: str):
        async with self.lock:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
            self.connection_counter -= 1
            logger.info(f"Connection closed in session {session_id}. Total connections: {self.connection_counter}")

    async def broadcast_to_session(self, message: dict, session_id: str):
        if session_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[session_id]:
                try:
                    if connection.client_state == WebSocketState.CONNECTED:
                        await connection.send_text(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    disconnected.add(connection)
            
            # 清理断开的连接
            if disconnected:
                async with self.lock:
                    for conn in disconnected:
                        await self.disconnect(conn, session_id)

    async def broadcast_message_worker(self):
        """后台任务,处理消息队列"""
        while True:
            try:
                message, session_id = await self.message_queue.get()
                await self.broadcast_to_session(message, session_id)
                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Error in broadcast worker: {e}")

    def get_session_connections_count(self, session_id: str) -> int:
        return len(self.active_connections.get(session_id, set()))