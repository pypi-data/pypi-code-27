import asyncio
import pytest
from redis_relay import get_id, get_id2


def test_get_id():
    assert len(get_id()) == 12


def test_get_id2():
    assert len(get_id2()) == 32


class Handler:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.counter = 0

    async def on_incr(self, num):
        self.counter += num

    async def on_slow(self, x=1):
        await asyncio.sleep(x)


@pytest.mark.asyncio
async def test_login(relay):
    handler = Handler()
    handler2 = Handler()
    await relay.login("001", handler)
    await relay.call_incr("001", 3)
    await asyncio.sleep(0.1)
    assert handler.counter == 3
    await relay.call_none("001", 3)
    await relay.call_incr("001", 2)
    await relay.call_slow("001")
    await asyncio.sleep(0.5)
    assert handler.counter == 5
    await relay.login("001", handler2)
    await asyncio.sleep(0.1)
    await relay.call_incr("001", 2)
    await asyncio.sleep(0.1)
    assert handler.counter == 5
    assert handler2.counter == 2
    await relay.call_slow("001", 3)
    await relay.stop()


@pytest.mark.asyncio
async def test_logout(relay):
    await relay.logout("001")
    await relay.logout("002")


@pytest.mark.asyncio
async def test_call(relay):
    await relay.call_beep("001", "a", b=3)


@pytest.mark.asyncio
async def test_bad_call(relay):
    with pytest.raises(AttributeError):
        await relay.bad_call("001")
