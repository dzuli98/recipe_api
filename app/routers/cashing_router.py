from typing import List
from fastapi import APIRouter
import time
import asyncio
from ..core.redis_client import redis_client
import json

router = APIRouter(prefix="/cashing",
                   tags=["Cashing"])

async def get_very_slow_report():
    """Simulates a slow, blocking I/O operation like a database query"""
    print("--- Running a slow data query... --- ")
    await asyncio.sleep(3)
    return {"report_id": "xyz-123", "data":[1,2,3]}

@router.get('/slow-report')
async def get_slow_report_endpoint():
    # define a unique key for this endpoint cache
    cache_key = "reports:slow_report"
    # check the cache first

    try:
        cached_report = await redis_client.client.get(cache_key)
        if cached_report:
            print("Cache hit")
            print('!!!!!!!!!!!!! CACHE', type(cached_report))
            return json.loads(cached_report)
    except Exception as e:
        print("Redis error (GET):", e)
        print("Redis is down!")

    print('Cache Miss!')
    report_data = await get_very_slow_report()

    # store result in redis for the next time
    # ex=30 sets a Time to Live (TTL) of 30 sec! This is CRITICAL!
    await redis_client.client.set(cache_key, json.dumps(report_data), ex=30)
    return report_data