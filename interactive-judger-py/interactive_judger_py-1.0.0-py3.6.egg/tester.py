import importlib
import signal
import os
import sys
from .judge_result import Result
from .built_in_judger import equality_judger


class TimeLimitExceededError(AssertionError):
    def __init__(self, error_message=''):
        self.value = error_message

    def __str__(self):
        return repr(self.value)


class Tester:
    __slots__ = ['program_name', 'method_name', 'precision_resolver', 'judge_method',
                 'time_limit', 'src_path']

    def __init__(self):
        pass

    def __init__(self, program_name: str, src_path: str, method_name: str, time_limit=10,
                 precision_resolver=None, judger=equality_judger):
        self.program_name = program_name
        self.method_name = method_name
        self.src_path = src_path
        self.precision_resolver = precision_resolver
        self.judge_method = judger
        self.time_limit = time_limit

    def set_program(self, program):
        self.program_name = program

    def set_method(selfs, method):
        self.method_name = method

    def set_judger(self, judger_method):
        self.judger = judger_method

    def run_test(self, test_data: tuple, expected_answer):
        if test_data and expected_answer is not None and self.program_name is not None:
            if self.src_path not in sys.path:
                sys.path.append(self.src_path)
            try:
                prog = importlib.import_module(self.program_name)
            except ModuleNotFoundError:
                print('Module {} not found. Try to remove the suffix(.py)'.format(self.program_name))
                return Result.JE

            def run(func):
                def handler(signum, frame):
                    raise TimeLimitExceededError()

                old = signal.signal(signal.SIGALRM, handler)
                signal.setitimer(signal.ITIMER_REAL, self.time_limit)
                try:
                    result = func(*test_data)
                    return result
                except TimeLimitExceededError:
                    return Result.TLE
                except:
                    return Result.RE
                finally:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                    signal.signal(signal.SIGALRM, old)

            result = run(eval(f'prog.{self.method_name}'))
            if isinstance(result, Result):
                return result
            if self.precision_resolver:
                result = self.precision_resolver(result)
            return self.judge_method(expected=expected_answer, actual=result)
        else:
            raise Exception('Data insufficient')
