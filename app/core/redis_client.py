import redis.asyncio as redis

# create single reusable connection
# decode_responses makes it return strings instead of bytes
class RedisClient():
    def __init__(self):
        self.client = redis.Redis(
                host = 'localhost',
                port = 6379,
                db = 0,
                decode_responses=True
            )           

    async def check_redis_connection(self):
        try:
            await self.client.ping()
            print(f'✅ Successfully connected to redis!')
        except redis.exceptions.ConnectionError as e:
            print(f'❌ Could not connect to redis {e}')
            exit()

redis_client = RedisClient()