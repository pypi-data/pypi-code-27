import inspect
import time
from datetime import datetime
import logging
from threading import Lock


class Task(object):

    def __init__(self, func, dependencies, options, **kwargs):
        """
        @type func: 0-ary function
        @type dependencies: list of Task objects
        """
        self.func = func
        self.name = func.__name__
        self.doc = inspect.getdoc(func) or ''
        self.dependencies = dependencies
        self.ignored = bool(options.get('ignore', False))
        self.async_task = kwargs.get('async_task', False)
        self.logger = None

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        if self.logger:
            if self.async_task:
                self.logger.info("Starting async task \"{}\" in background".format(self.name))
            else:
                self.logger.info("Starting task \"{}\"".format(self.name))

        t = datetime.now()

        self.result = self.func.__call__(*args, **kwargs)

        if self.logger:
            self.logger.info("Completed task \"{task_name}\". Time: {run_time} sec".format(
                    task_name=self.name, run_time=(datetime.now() - t).seconds
                )
            )

        return self.result

    def set_future(self, future):
        self.future = future

    def set_logger(self, logger):
        self.logger = logger

    @classmethod
    def is_task(cls, obj):
        """
        Returns true is an object is a build task.
        """
        return isinstance(obj, cls)


class CurrentThreadExecutor(object):

    def __init__(self):
        pass

    def submit(self, task, *args, **kwargs):
        task(*(args or []), **(kwargs or {}))
        return PseudoFutureTask()


class PseudoFutureTask(object):

    def __init__(self):
        pass

    def running(self):
        return False
