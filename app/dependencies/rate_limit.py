from fastapi import HTTPException, Request, status
from redis.asyncio import RedisError
from ..core.redis_client import redis_client
from ..settings import settings
import time

'''
The “burst at the boundary” problem
Window 1: 12:00:00 → 12:00:59
User makes 60 requests — the limit is reached.
Window 2: 12:01:00 → 12:01:59
Right after the new window starts, the user can make another 60 requests
'''
async def fixed_window_rate_limiter(request: Request):
    # use client's IP address as a unique identifier
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host

        key = f"rate_limit:{client_ip}"

        try:
            # Increment request count
            current_count = await redis_client.client.incr(key)
            if current_count == 1:
                # Set expiration for first request in window
                await redis_client.client.expire(key, settings.settings.window_size)

            if current_count > settings.settings.max_requests_per_minute:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Too many requests. Limit is {settings.settings.max_requests_per_minute} per {settings.settings.window_size} seconds."
                )

        except RedisError as e:
            # Fail open if Redis is down
            print("Rate limiter Redis unavailable:", e)
            

async def sliding_window_rate_limiter(request: Request):
    """
    Sliding window rate limiter:
    - Uses Redis sorted set to track timestamps of requests
    - Limits requests to `settings.max_requests_per_minute` per `settings.window_size` seconds
    """
    try:
        # 1. Get client IP (handle X-Forwarded-For)
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host

        key = f"rate_limit_sw:{client_ip}"

        now = int(time.time())
        window_start = now - settings.window_size

        # 2. Remove old entries outside the window
        await redis_client.client.zremrangebyscore(key, 0, window_start)

        # 3. Count requests in the current window
        current_count = await redis_client.client.zcard(key)

        if current_count >= settings.max_requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests. Limit is {settings.max_requests_per_minute} per {settings.window_size} seconds."
            )

        # 4. Add current request timestamp
        await redis_client.client.zadd(key, {str(now): now})

        # 5. Set expiration slightly longer than window
        await redis_client.client.expire(key, settings.window_size + 5)

    except RedisError as e:
        # Fail open if Redis is down
        print("Rate limiter Redis unavailable:", e)
        return

def rate_limit_user(key:str , limit: int, window: int) -> bool:
    """
    Synchronous rate limiter for non-async contexts.
    - key: Unique identifier (e.g., user ID)
    - limit: Max requests allowed
    - window: Time window in seconds
    """
    try:
        current_count = redis_client.client.incr(key)
        if current_count == 1:
            redis_client.client.expire(key, window)

        if current_count > limit:
            return False  # Rate limit exceeded

        return True  # Within rate limit

    except RedisError as e:
        print("Rate limiter Redis unavailable:", e)
        return True  # Fail open