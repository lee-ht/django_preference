import json

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views import View

from apps.app.constants import REDIS_TTL
from apps.app.models import RawData
from kafka_config import AIOKafka
from rabbitmq_config import RabbitMQ_CONF
from utils.jsons import obj_to_json


class Files(View):
    async def get(self, request):
        return HttpResponse('file')


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


class KafkaConnect(View):
    async def get(self, request):
        while True:
            msg = await aiokafka.get_single_msg()
            print(msg)

        return JsonResponse(msg)

    async def post(self, request):
        body = json.loads(request.body)
        await aiokafka.send_msg(body)

        return JsonResponse(body)


rabbitmq = RabbitMQ_CONF()


class RabbitMQ(View):
    async def get(self, request):
        msg = await rabbitmq.get_single_msg()

        return HttpResponse(msg)

    async def post(self, request):
        body = request.body
        await rabbitmq.send_msg(body)

        return HttpResponse('')
