"""
@file: consumer.py
@author: Runpu
@time: 2023/5/23 21:27
"""
import pdb
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .controller import handle_message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("已连接")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        res = handle_message(text_data)
        await self.send(text_data=res)
