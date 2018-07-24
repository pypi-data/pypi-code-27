import sys
from tblib import Traceback
from six import reraise
from multiprocessing import Process, Queue
from multiprocessing.queues import Empty


class InterfacedProcess(Process):

    def __init__(self):
        super().__init__()
        self._exc = Queue(maxsize=1)
        self._ret = Queue(maxsize=1)

    def run(self):
        try:
            self._ret.put( self.try_run() )
        except BaseException as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self._exc.put( (exc_type, exc_value, Traceback(exc_traceback)) )

    def reraise(self):
        try:
            exc_type, exc_value, exc_traceback = self._exc.get(block=False)
        except Empty:
            pass
        else:
            reraise(exc_type, exc_value, exc_traceback.as_traceback())

    def get_retval(self):
        self.join()
        try:
            return self._ret.get(block=False)
        except Empty:
            pass

    def is_alive(self):
        self.reraise()
        return super().is_alive()

    def join(self):
        super().join()
        self.reraise()


class working(InterfacedProcess):

    def __init__(self, target, args=(), kwargs={}):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        super().__init__()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_value:
            self.terminate()
        self.join()

    def try_run(self):
        return self.target(*self.args, **self.kwargs)

    def __call__(self):
        return self.get_retval()

    def __bool__(self):
        return self.is_alive()

    def __len__(self):
        return len(self.target)

    def __iter__(self):
        yield from self.target
