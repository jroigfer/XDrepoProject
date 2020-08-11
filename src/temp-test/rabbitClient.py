import pika
import sys

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('10.86.22.36',
                                       5673,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='test4')

channel.basic_publish(exchange='',
                      routing_key='test6',
                      body="hola")

channel.basic_publish(exchange='',
                      routing_key='test7',
                      body="hola2")

#channel.exchange_declare(exchange='logs', exchange_type='fanout')

#message = ' '.join(sys.argv[1:]) or "info: Hello World!"
#channel.basic_publish(exchange='logs', routing_key='', body=message)
#print(" [x] Sent %r" % message)
connection.close()