import inspect
# import cProfile
import traceback
from datetime import datetime
from collections import namedtuple


class TestFailure(AssertionError):
    pass


class SpeedTestFailure(AssertionError):
    pass


class Result(namedtuple('Result', 'name result message tb')):
    PASS = 'pass'
    FAIL = 'fail'
    ERROR = 'error'


class SuiteType(type):
    SUITES = []

    def __new__(mcls, name, bases, dct):
        cls = super(SuiteType, mcls).__new__(mcls, name, bases, dct)
        SuiteType.SUITES.append((name, cls))
        return cls


class Suite(metaclass=SuiteType):

    def _iter_tests(self):
        methods = {
            name: func
            for name, func in inspect.getmembers(self)
            if name.startswith('test_')
        }
        for name, func in methods.items():
            yield name, func

    def _add_result(self, result, message=None, tb=None):
        result = Result(self.current_test, result, message, tb)
        self.results.append(result)
        return result

    def run(self):
        self.results = []
        for name, func in self._iter_tests():
            self.current_test = name
            self.setup()
            try:
                func()
                yield self._add_result(Result.PASS)
            except SpeedTestFailure as e:
                yield self._add_result(Result.FAIL, message=e.args[0])
            except TestFailure as e:
                yield self._add_result(Result.FAIL, message=e.args[0])
            except KeyboardInterrupt:
                print('ctrl-c')
                break
            except Exception as e:
                tb = traceback.format_exc()
                yield self._add_result(Result.ERROR, message=str(e), tb=tb)
            self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass

    def assert_true(self, cond, message=None):
        if not cond:
            raise TestFailure(message)

    def faster_than(self, s=1.0, ms=0.0):
        seconds = s + ms * 1000

        class FasterThan:
            def __init__(self, seconds):
                self.seconds = seconds

            def __enter__(self):
                self.start = datetime.now()

            def __exit__(self, *args):
                self.end = datetime.now()
                td = self.end - self.start
                self.time = td.seconds + (td.microseconds / 1000000.0)
                if self.time >= self.seconds:
                    raise SpeedTestFailure(
                        'took {:.3f} seconds, should be less than {:.3f} '
                        'seconds'.format(self.time, self.seconds)
                    )

        return FasterThan(seconds)
