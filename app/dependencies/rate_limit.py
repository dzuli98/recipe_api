from fastapi import HTTPException, Request, status
from redis.asyncio import RedisError
from ..core.redis_client import redis_client
from .. import settings

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
            return
