import aioredis
import os

redis = aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

async def cache_user(user_id, data):
    await redis.setex(f"user:{user_id}", 3600, data)
