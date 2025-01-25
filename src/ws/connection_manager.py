from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Tuple
import asyncio
from datetime import datetime
from dataclasses import dataclass, asdict

from fastapi.websockets import WebSocketState

from src.util.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    def __init__(self):
        # 存储所有活跃连接，键为 (user_id, character_id) 的元组
        self.active_connections: Dict[Tuple[str, str], Set[WebSocket]] = {}
        # 消息队列
        self.message_queue: asyncio.Queue = asyncio.Queue()
        # 连接计数器
        self.connection_counter = 0
        # 锁,用于保护共享资源
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: str, character_id: str):
        try:
            await websocket.accept()
            async with self.lock:
                connection_key = (user_id, character_id)
                if connection_key not in self.active_connections:
                    self.active_connections[connection_key] = set()
                self.active_connections[connection_key].add(websocket)
                self.connection_counter += 1
                logger.info(f"New connection for user {user_id} and character {character_id}. Total connections: {self.connection_counter}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")

    async def disconnect(self, websocket: WebSocket, user_id: str, character_id: str):
        connection_key = (user_id, character_id)
        async with self.lock:
            if connection_key in self.active_connections:
                self.active_connections[connection_key].remove(websocket)
                if not self.active_connections[connection_key]:
                    del self.active_connections[connection_key]
                self.connection_counter -= 1
                logger.info(f"Connection closed for user {user_id} and character {character_id}. Total connections: {self.connection_counter}")

    async def broadcast_to_user_character(self, message: dict, user_id: str, character_id: str):
        connection_key = (user_id, character_id)
        if connection_key in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[connection_key]:
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
                        await self.disconnect(conn, user_id, character_id)

    async def broadcast_message_worker(self):
        """后台任务,处理消息队列"""
        while True:
            try:
                message, user_id, character_id = await self.message_queue.get()
                await self.broadcast_to_user_character(message, user_id, character_id)
                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Error in broadcast worker: {e}")

    def get_user_character_connections_count(self, user_id: str, character_id: str) -> int:
        connection_key = (user_id, character_id)
        return len(self.active_connections.get(connection_key, set()))