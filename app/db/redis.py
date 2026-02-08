import redis.asyncio as redis
from app.core.config import settings


class RedisClient:
    _client: redis.Redis = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.from_url(
                settings.REDIS_URI, encoding="utf-8", decode_responses=True
            )
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.close()


async def get_redis() -> redis.Redis:
    return RedisClient.get_client()
