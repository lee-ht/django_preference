import json
import os

from kafka import KafkaProducer, KafkaConsumer

from config.settings import env


class KafkaConfig:
    def __init__(self):
        print("Connecting Kafka : ", end="")
        self.__producer = KafkaProducer(
            acks=1,
            compression_type='gzip',
            bootstrap_servers=[env("KAFKA_URL")],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            batch_size=1,
        )
        print(self.__producer.bootstrap_connected(), end=", ")
        # topic 여러개 생성시 dict key: topic , value: consumer
        self.__consumer = KafkaConsumer(
            "RawData",
            bootstrap_servers=[env("KAFKA_URL")],
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            consumer_timeout_ms=10000,
            # auto_offset_reset='earliest',
        )
        print(self.__consumer.bootstrap_connected())

    async def send_msg(self, value: dict, topic="RawData"):
        self.__producer.send(topic, value)
        self.__producer.flush()

    async def get_msgs(self):
        response = self.__consumer.poll(timeout_ms=10000)
        for row in response.values():
            data = row[0].value
        # for message in self.__consumer:
        #     print(f"{message.topic},{message.key},{message.value}")
