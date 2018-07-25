from core.base_job import BaseJob
from random import randint
import schedule
import time

class TestJob(BaseJob):
    """
    测试任务
    """

    def run(self, *args, **kwargs):
        print('in TestJob', args, kwargs)
        time.sleep(randint(1,4))
        self.logger.debug("hello from %d" % args[0])

    def schedule(self):
        return schedule.every(2).seconds.do
