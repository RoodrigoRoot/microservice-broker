from calendar import c
import queue

from django.db import connection
import pika, json
from abc import ABC, abstractmethod

class Broker(ABC):

    @abstractmethod
    def connection(self):
        raise NotImplementedError()

    @abstractmethod
    def connection_is_alive(self):
        raise NotImplementedError()

    @abstractmethod
    def publish(self):
        raise NotImplementedError()

class BrokerCredentials(Broker):

    user: str
    password: str
    queue: str
    port: int
    vhost: str


class RabbitMQBroker(BrokerCredentials):

    def connection(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('broker',
                                                5672,
                                                '/',
                                                credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="notifications", durable=True, exclusive=False, auto_delete=False)
        self.channel.confirm_delivery()

    def connection_is_alive(self) -> bool:
        return not self.connection.is_closed


    def publish(self, body: dict):
        try:
            if not self.connection_is_alive or self.connection:
                self.connection()
                self.channel.basic_publish(exchange='',
                                    routing_key='notifications',
                                    body=json.dumps(body),
                                    properties=pika.BasicProperties(content_type='application/json',
                                                                    delivery_mode=1))
                print('Message publish was confirmed')
            else:
                self.connection()
                self.publish(body)
        except pika.exceptions.UnroutableError:
            print('Message could not be confirmed')

