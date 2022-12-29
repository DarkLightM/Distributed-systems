import json
import os

from app import models
import pika

connection = pika.BlockingConnection(pika.URLParameters(os.environ['RABBITMQ_URL']))
channel = connection.channel()


def send_message_to_queue(link: models.Link) -> None:
    channel.queue_declare(queue=os.environ['QUEUE_NAME'])
    channel.basic_publish(exchange='', routing_key=os.environ['QUEUE_NAME'], body=json.dumps({
        'id': link.id,
        'url': link.url
    }).encode('utf-8'))
