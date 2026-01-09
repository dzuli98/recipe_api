from .celery_app import celery_app
from kombu import Exchange, Queue

# configuration
celery_app.conf.update(
    autodiscover_tasks=['app.tasks'],
    # task serialization
    task_serialization='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,

    # task execution settings
    task_acks_late=True, # acknowledge tasks after execution
    task_reject_on_worker_lost=True, # requeue tasks if worker crashes
    task_track_started=True, # track when tasks start

    # result backend settings
    result_expires=3600, # results expire in 1 hour
    result_persistent=True, # persist results

    # connection settings
    broker_connection_retry_on_startup=True, # retry on startup
    broker_connection_max_retries=5, # try 5 times to connect to redis
    broker_connection_retry = True, # enable retries during runtime

    #worker settings
    worker_prefetch_multiplier=1, # disable prefetching
    worker_max_tasks_per_child=100, # restart worker after 100 tasks

    # task routing with priority queues
    task_queues = (
        Queue('high_priority', Exchange('high_priority'), routing_key='high_priority', max_priority=10),
        Queue('default', Exchange('default'), routing_key='default', max_priority=5),
        Queue('low_priority', Exchange('low_priority'), routing_key='low_priority', max_priority=1),
    ),
    task_default_queue='default',
    task_default_exchange='default',
    task_default_routing_key='default',

    # rate limiting
    task_default_rate_limit='100/m', # default rate limit

    # retry policy defaults

    # Task fails -> Celery waits (with backoff + jitter) -> Retry happens -> Max 5 retries -> If still failing → give up
    task_autoretry_for=(Exception,), # retry on all exceptions
    task_retry_backoff=True, # exponential backoff
    task_retry_backoff_max=600, # max backoff time
    task_retry_jitter=True, # add jitter to backoff
    task_retry_kwargs={'max_retries': 5}, # max 5 retries
)

# Force autodiscover to ensure tasks are registered
celery_app.autodiscover_tasks(['app.tasks'], force=True)
