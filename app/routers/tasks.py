from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from .. celery_worker import create_task


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/ex1")
def run_task(data=Body(...)):
    amount = int(data['amount'])
    x = data['x']
    y = data['y']
    task = create_task.delay(amount, x, y)
    return JSONResponse({'Task': task.get()})
