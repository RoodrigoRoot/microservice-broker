import pika, json

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('broker',
                                   5672,
                                   '/',
                                   credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="notifications", durable=True, exclusive=False, auto_delete=False)
channel.confirm_delivery()

def publish(body: dict):
    try:
        channel.basic_publish(exchange='',
                            routing_key='notifications',
                            body=json.dumps(body),
                            properties=pika.BasicProperties(content_type='application/json',
                                                            delivery_mode=1))
        print('Message publish was confirmed')
    except pika.exceptions.UnroutableError:
        print('Message could not be confirmed')


connection.close()
