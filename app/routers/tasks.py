from celery.result import AsyncResult
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.responses import JSONResponse
from app import tasks
from .. schemas import EmailRequest
from ..celery_app import celery_app
from ..dependencies.rate_limit import rate_limit_user
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/tasks", tags=["Tasks"])

'''async def rate_limit_check(user_id: str):
    if not rate_limit_user(f'rate_limit:{user_id}', limit=5, window=60):
        raise HTTPException(
            status_code=429,
            detail="Too many requests, please try again later."
        )
    return user_id
'''

@router.post("/ex1")
def run_task(data=Body(...)):
    amount = int(data['amount'])
    x = data['x']
    y = data['y']
    task = tasks.create_task.delay(amount, x, y)
    return JSONResponse({'Task': task.get()})

@router.post('/send-email')
async def send_email(request: EmailRequest):
    task = tasks.send_email_task.apply_async(
        args=[request.recipient, request.subject, request.body],
        priority=9)
    return {'task_id': task.id, 'status': 'Email task submitted'}

@router.get('/task-status/{task_id}')
async def get_task_status(task_id: str):
    task = AsyncResult(task_id, app= celery_app )
    if task.state == 'PENDING':
        return {'task_id': task_id, 'status': 'Pending'}
    elif task.state == 'SUCCESS':
        return {'task_id': task_id, 'status': 'Completed', 'result': task.result}
    elif task.state == 'PROGRESS':
        return {'task_id': task_id, 'status': task.info.get('status','')}
    elif task.state == 'FAILURE':
        return {'task_id': task_id, 'status': 'Failed', 'error': str(task.info)}
    else:
        return {'task_id': task_id, 'status': task.state}