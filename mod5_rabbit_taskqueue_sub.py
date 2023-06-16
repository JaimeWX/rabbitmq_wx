import pika
import time

credentials = pika.PlainCredentials('guest','guest')

parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    time.sleep(1)
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)

# 如果该消费者的channel上未确认的消息数达到了prefetch_count数，则不向该消费者发送消息
channel.basic_qos(prefetch_count=1)

channel.basic_consume('task_queue', callback)

channel.start_consuming()


    