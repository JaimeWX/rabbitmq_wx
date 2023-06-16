import pika

credentials = pika.PlainCredentials('guest','guest')

parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True) # 队列持久化

message = 'send message to taskqueue'
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(delivery_mode=2)) # 消息持久化

connection.close()

