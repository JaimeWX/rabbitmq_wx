''' 
    两边都声明队列
'''

import pika

credentials = pika.PlainCredentials('guest','guest') # 不同的业务分配不同的用户名和密码

# 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填
parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

# 阻塞方法
connection = pika.BlockingConnection(parameters=parameters)

# 建立信道
channel = connection.channel()

# 声明消息队列
# 如不存在自动创建
# durable=True 队列持久化
channel.queue_declare(queue='direct_demo', durable=False)

# exchange指定交换机
# routing_key指定队列名
channel.basic_publish(exchange='', routing_key='direct_demo', # routing_key标识使用哪一个队列
                      body='send message2 to rabbitmq') # 实际上发的消息一般是json或xml格式的

# 关闭与rabbitmq server的连接
connection.close()