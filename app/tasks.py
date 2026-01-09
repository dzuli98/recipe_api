from app.celery_app import celery_app
from celery.utils.log import get_task_logger
from typing import Dict
import time

# ==============Send Email ============== #

'''
Logger used specifically for Celery tasks
Works inside tasks (@celery.task)
Automatically formats logs with task ID, name, retries, etc.
'''
logger = get_task_logger(__name__)

@celery_app.task(
    bind=True,
    name='create_task'
)
def create_task(self, a, b, c):
    time.sleep(a)
    return b + c

@celery_app.task(
    bind=True,
    max_retries=3,
    name='send_email',
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    queue='high_priority'
)
def send_email_task(self, recipient: str, subject: str, body: str) -> bool: # self is the task instance
    """
    Simulates sending an email.
    In a real implementation, integrate with an email service provider.
    """
    try:
        logger.info(f"Sending email to {recipient} with subject '{subject}'")
        # Simulate email sending delay
        time.sleep(2)
        logger.info(f"Email sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {str(e)}")
        raise self.retry(exc=e)

# ==============Data Processing ============== #
@celery_app.task(
    bind=True,
    name='process_data',
    max_retries=2,
    time_limit=3600, # kill the task if it runs longer than 1 hour
    soft_time_limit=3500,
    queue='low_priority'
)
def process_data(self, file_path: str) -> Dict:
    """
    Process large file in the background.
    Use case: csv imports, data migrations, reports generation, etc.
    """
    try:
        logger.info(f"Processing data file at {file_path}")
        # Simulate data processing delay
        self.update_state(
            state='PROGRESS',
            meta={'status': 'Starting data processing'})
        # simulate processing
        for i in range(5):
            time.sleep(1)  # simulate time-consuming processing
            self.update_state(
                state='PROGRESS',
                meta={'status': f'Processing {i}/5'})
        logger.info(f"Data processing completed for file {file_path}")
        return {'status': 'Completed', 'file_path': file_path}
    except Exception as e:
        logger.error(f"Failed to process data file {file_path}: {str(e)}")
        raise self.retry(exc=e)