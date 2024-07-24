import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache


class Websocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        cache.set("start_time", datetime.now())
        await self.accept()

    async def disconnect(self, close_code):
        cache.set("operation_time", datetime.now() - cache.get("start_time"))
        print(cache.get("operation_time"))

    # async def receive_json(self, content, **kwargs):
    #     await self.send_json(content=content)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        json_data = json.loads(text_data)
        if text_data is not None:
            await self.send_json(content=json_data)
        if bytes_data is not None:
            print("get binary data")
            await self.send(bytes_data=bytes_data)
