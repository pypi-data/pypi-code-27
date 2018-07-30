import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import datetime
import queue

from .thread import thread_spawn


class AsyncWorker(object):
    def __init__(self, pool_size=8, queue_size=0):
        """
        :param pool_size:
        :param queue_size: If <= 0, the queue size is infinite.
        """
        self.pool_size = pool_size
        self.executor = None
        self._lock = threading.Lock()

        # for background poll
        self.done = False
        self._q = queue.Queue(queue_size)

    def init_pool(self):
        with self._lock:
            if not self.executor:
                self.executor = ThreadPoolExecutor(max_workers=self.pool_size)

    async def run_in_thread_pool(self, func, *args):
        """sync to async"""
        self.init_pool()
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(self.executor, func, *args)
        return result

    @staticmethod
    def run_coroutine_in_new_event_loop(coro):
        """async to sync: blocked"""
        loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        result = loop.run_until_complete(coro)
        return result

    @staticmethod
    def run_in_thread(func, name=None):
        """run function in thread"""
        thread_spawn(
            func, name
            or '{} {}'.format(func.__name__, str(datetime.datetime.now())))

    async def poll_tasks(self):
        while not self.done:
            task = self._q.get()
            await self.run_in_thread_pool(task)

    def start(self):
        def f():
            self.run_coroutine_in_new_event_loop(self.poll_tasks())

        self.run_in_thread(f, name='background_tasks_poll')

    def add_background_task(self, func, *args):
        from functools import wraps

        @wraps(func)
        def new_func():
            func(*args)

        with self._lock:
            self._q.put(new_func)
