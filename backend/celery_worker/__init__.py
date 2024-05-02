

import os

from celery import Celery


# celery
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_queue_db = os.environ.get('REDIS_QUEUE_DB')

redis_url = f'redis://{redis_host}:{redis_port}/{redis_queue_db}'

app = Celery('notification', backend=redis_url, broker=redis_url)
api_key = os.environ.get('API_KEY')


from celery_worker.tasks import *