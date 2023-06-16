import pika

credentials = pika.PlainCredentials('guest','guest')

parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

# 声明交换机
channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

# 声明消息队列
# exclusive 当与消费者断开连接的时候，队列被立即删除
res = channel.queue_declare(queue='',
                            exclusive=True)
queue_name = res.method.queue

# 通过bind实现exchange将message发送到指定的queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)

def callback(ch, method, properties, body):
    print(body.decode())
    # ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
# 消费者使用队列和哪个回调函数处理消息
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()