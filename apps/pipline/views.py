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


class WebsocketCh(AsyncJsonWebsocketConsumer):
    '''
    channels 로 메시지를 룸으로 전달
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    async def connect(self):
        self.room_group_name = f'ch_{self.scope["url_route"]["kwargs"]["room_name"]}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print(json.loads(text_data))
        await self.channel_layer.group_send(
            'ch1', {'type': 'chat.message', 'message': json.loads(text_data)}
        )


class WebsocketResponse(AsyncJsonWebsocketConsumer):
    '''
    channels 로 메시지 응답
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    async def connect(self):
        self.room_group_name = f'ch1'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))
