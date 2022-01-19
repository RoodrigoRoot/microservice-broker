import pika


credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('broker',
                                   5672,
                                   '/',
                                   credentials)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="notifications", durable=True, exclusive=False, auto_delete=False)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
