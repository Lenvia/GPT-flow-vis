"""
@file: consumer.py
@author: Runpu
@time: 2023/5/23 21:27
"""
import json
import pdb
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .controller import handle_message
from server import connection


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        connection.active_consumer = self  # 当前连接
        print("Websocket已连接")

    async def disconnect(self, close_code):
        print("Websocket已断开")

    async def receive(self, text_data):
        res = handle_message(text_data)

        if res is not None:
            # print(res)
            await self.send(text_data=json.dumps(res))
