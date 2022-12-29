import json
import os
import sys
from typing import Optional

import pika
import requests
import redis

QUEUE_NAME = os.environ['QUEUE_NAME']


cache = redis.Redis(os.environ['CACHE_HOST'], decode_responses=True)


def fetch_status_from_internet(url: str) -> int:
    response = requests.get(url, timeout=10)
    status = response.status_code
    return status


def get_from_cache(cache_key: str) -> Optional[int]:
    return cache.get(cache_key)


def set_cache(cache_key: str, status_code: int) -> None:
    cache.set(cache_key, status_code, ex=100)


def get_status(url: str) -> int:
    cache_key = f"url-{url}"

    status_code = get_from_cache(cache_key)
    if status_code is None:
        status_code = fetch_status_from_internet(url)
        set_cache(cache_key, status_code)
    return status_code


def handle_message(ch, method, properties, body):
    link_json = json.loads(body.decode('utf-8'))

    status = get_status(link_json['url'])

    web_url = f"{os.environ['WEB_BASE_URL']}/links/{link_json['id']}"
    web_request_body = {
        'status': str(status)
    }
    web_response = requests.put(web_url, json=web_request_body, timeout=10)
    web_response.raise_for_status()


def main():
    connection = pika.BlockingConnection(pika.URLParameters(os.environ['RABBITMQ_URL']))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME,
                          auto_ack=True,
                          on_message_callback=handle_message)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
