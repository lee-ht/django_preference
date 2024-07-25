import asyncio
import json
import logging

import aio_pika
import pika
from aio_pika import Message
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views import View

from apps.app.constants import REDIS_TTL
from apps.app.models import RawData
from kafka_config import KafkaConfig, AIOKafka
from utils.jsons import obj_to_json


class GetFiles(View):
    async def get(self, request):
        return HttpResponse('')


class Redis(View):
    async def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        key = body['key']
        value = body['value']

        cache.set(key, value, timeout=REDIS_TTL)
        data = cache.get(key)
        return JsonResponse({key: data})


class Database(View):
    async def get(self, request, name):
        # raws = RawData.objects.filter(name=name)
        raws = RawData.objects.all()
        data = obj_to_json(raws)

        return JsonResponse(data, safe=False)

    async def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        raws = RawData()
        raws.name = body['name']
        raws.value = body['value']

        raws.save()

        return HttpResponse('', status=200)

    async def delete(self, request):
        raws = RawData.objects.all()
        raws.delete()

        return HttpResponse('', status=204)


# kafka_conf = KafkaConfig()
aiokafka = AIOKafka()


class Broker(View):
    async def get(self, request):
        msg = await aiokafka.get_single_msg()

        return JsonResponse(msg)

    async def post(self, request):
        body = json.loads(request.body)
        await aiokafka.send_msg(body)

        return JsonResponse(body)


class RabbitMQ(View):
    async def get(self, request):
        qname = "RawData"
        conn = await aio_pika.connect_robust(
            "amqp://localhost"
        )
        async with conn:
            channel = await conn.channel()

            queue = await channel.declare_queue(qname)

            async def process_message(message):
                async with message.process():
                    print(f"{message.body.decode()}")

            await queue.consume(process_message)

            await asyncio.Future()
        return HttpResponse('')

    async def post(self, request):
        body = request.body
        qname = "RawData"
        connection = await aio_pika.connect_robust(
            "amqp://localhost",
        )

        async with connection:
            channel = await connection.channel()

            message = Message(body)
            await channel.default_exchange.publish(message, routing_key=qname)
            print("전송 완료")

        return HttpResponse('')
