"redis relay for interprocess communication"
import os
import uuid
import base64
import pickle
import asyncio
import weakref
import logging
import inspect

__version__ = "0.0.1"
logger = logging.getLogger(__name__)


def get_id():
    ident = (uuid.getnode() << 16) + os.getpid()
    ident = base64.urlsafe_b64encode(ident.to_bytes(8, "big"))
    ident = ident.decode()
    return ident


def get_id2():
    return uuid.uuid4().hex


async def lock_run(coro, lock):
    async with lock:
        return await coro


class RedisRelay:
    ident_hkey = "ident-channel-map"

    def __init__(self, redis, loop):
        self.redis = redis
        self.channel_id = "ch:{}".format(get_id())
        self.tasks = set()
        self.handlers = weakref.WeakValueDictionary()
        self.main_task = loop.create_task(self.run(loop))

    async def run(self, loop):
        channel, = await self.redis.subscribe(self.channel_id)
        self.ch = channel
        async for data in channel.iter():
            try:
                message = pickle.loads(data)
                ident, method, args, kw = message
                handler = self.handlers[ident]
                coro = getattr(handler, "on_" + method)(*args, **kw)
                if inspect.isawaitable(coro):
                    if hasattr(handler, "lock"):
                        coro = lock_run(coro, handler.lock)
                    task = loop.create_task(coro)
                    self.tasks.add(task)
                    task.add_done_callback(self.tasks.remove)
            except Exception:
                logger.exception("channel data handling error")

    async def stop(self):
        try:
            await self.redis.unsubscribe(self.channel_id)
        finally:
            self.main_task.cancel()
            if self.tasks:
                await asyncio.wait(self.tasks)

    async def login(self, ident: str, handler) -> None:
        await self.redis.hset(self.ident_hkey, ident, self.channel_id)
        self.handlers[ident] = handler

    async def logout(self, ident: str) -> None:
        await self.redis.hdel(self.ident_hkey, ident)
        self.handlers.pop(ident, None)

    def __getattr__(self, name: str):
        if not name.startswith("call_"):
            raise AttributeError
        method = name[5:]

        async def func(ident, *args, **kw):
            channel_id = await self.redis.hget(self.ident_hkey, ident)
            if not channel_id:
                return False
            data = pickle.dumps([ident, method, args, kw])
            await self.redis.publish(channel_id, data)

        return func
