import pika

credentials = pika.PlainCredentials('guest','guest')

parameters = pika.ConnectionParameters(host='0.0.0.0',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)

connection = pika.BlockingConnection(parameters=parameters)

channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

message = 'send message to fanout'
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

connection.close()
