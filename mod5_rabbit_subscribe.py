import pika

credentials = pika.PlainCredentials('guest','guest')

parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.queue_declare(queue='direct_demo', durable=False)

# 定义一个回调函数来处理消息队列中的消息
def callback(ch, method, properties, body):
    # 手动发送确认消息
    ch.basic_ack(delivery_tag=method.delivery_tag) # ack确认，防止消息丢失
    # 实现如何处理消息
    print(body.decode())

# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume('direct_demo', on_message_callback=callback)

# 开始接收信息，并进入阻塞状态
channel.start_consuming()