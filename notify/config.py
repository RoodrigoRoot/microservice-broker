import os
from pydantic import BaseSettings


class Settings(BaseSettings):

    USER_RABBITMQ: str = os.getenv('USER_RABBITMQ', '')
    PASSWORD_RABBITMQ: str = os.getenv('PASSWORD_RABBITMQ', '')
    RABBITMQ_HOST: str = os.getenv('RABBITMQ_HOST', '')
    RABBITMQ_PORT: int = os.getenv('RABBITMQ_PORT', '')
    RABBITMQ_VHOST: str = os.getenv('RABBITMQ_VHOST', '')
    QUEUE_RABBITMQ: str = os.getenv('QUEUE_RABBITMQ', '')


settings = Settings()



