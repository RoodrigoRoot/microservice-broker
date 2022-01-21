import queue
import pika, json
from abc import ABC, abstractmethod
from django.conf import settings

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
    host: str
    port: int
    vhost: str


class RabbitMQBroker(BrokerCredentials):

    user: str = settings.USER_RABBITMQ
    password: str = settings.PASSWORD_RABBITMQ
    queue: str = settings.QUEUE_RABBITMQ
    vhost: str = settings.RABBITMQ_VHOST
    port: int = settings.RABBITMQ_PORT
    host: str = settings.RABBITMQ_HOST


    def connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(self.host,
                                                self.port,
                                                self.vhost,
                                                credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True, exclusive=False, auto_delete=False)
        self.channel.confirm_delivery()

    def connection_is_alive(self) -> bool:
        return not self.connection.is_closed


    def publish(self, body: dict):
        try:
            if not self.connection_is_alive or self.connection:
                self.connection()
                self.channel.basic_publish(exchange='',
                                    routing_key=self.queue,
                                    body=json.dumps(body),
                                    properties=pika.BasicProperties(content_type='application/json',
                                                                    delivery_mode=1))
            else:
                self.connection()
                self.publish(body)
        except pika.exceptions.UnroutableError:
            print('Message could not be confirmed')

