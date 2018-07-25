import pytest
import asyncio
import aioredis
from redis_relay import RedisRelay


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def redis(event_loop):
    r = await aioredis.create_redis_pool("redis://localhost", loop=event_loop)
    yield r
    r.close()
    await r.wait_closed()


@pytest.fixture(scope="session")
async def relay(redis, event_loop):
    relay = RedisRelay(redis, event_loop)
    yield relay
    await relay.stop()
