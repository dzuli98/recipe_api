from celery import Celery
import os

# initialize celery with redis as broker and backend
celery_app = Celery(
    'my_app',
    broker=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://redis:6379/0')
)