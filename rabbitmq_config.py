import asyncio

import aio_pika
from aio_pika import Message


class RabbitMQ_CONF:
    def __init__(self):
        self.__URL = "amqp://localhost"
        self.__queue_name = "RawData"

    async def send_msg(self, body):
        connection = await aio_pika.connect_robust(self.__URL)

        async with connection:
            channel = await connection.channel()

            message = Message(body)
            await channel.default_exchange.publish(message, routing_key=self.__queue_name)
            print("전송 완료")

    async def get_single_msg(self):
        conn = await aio_pika.connect_robust(self.__URL)

        async with conn:
            channel = await conn.channel()

            queue = await channel.declare_queue(self.__queue_name, auto_delete=True)
            # 동시 처리될 최대 메시지 수
            await channel.set_qos(prefetch_count=10)

            await queue.consume(self.process_message)

            # queue = await channel.declare_queue(self.__queue_name, auto_delete=True)
            # async with queue.iterator() as queue_iter:
            #     async for message in queue_iter:
            #         async with message.process():
            #             print(message.body.decode())
            #             print(queue.name)
            #
            #             # if queue.name in message.body.decode():
            #             #     break

            try:
                await asyncio.Future()
            finally:
                await conn.close()

    async def process_message(self, message):
        async with message.process():
            print(message.body.decode())
