#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import timeit
import itertools
import gc
import math
from . import utils
from ._core_validators import validate


try:
    if utils.is_interactive():
        from tqdm import tqdm_notebook as tqdm
    else:
        from tqdm import tqdm

except ImportError:
    tqdm = lambda x: x


class Dataset(object):
    '''Dataset class.

    Args:
        factories (list):
        extra_args (dict): Extra arguments to pass to Kernel.
            This parameter slightly affects measurement results.
    '''
    def __init__(self, factories, *, extra_args=None):
        self._factories = factories
        self._extra_args = extra_args

    @property
    def factories(self):
        return self._factories

    @property
    def extra_args(self):
        return self._extra_args


class Kernel(object):
    '''Kernel class.

    Args:
        stmt:
        setup:
    '''
    def __init__(self, stmt='pass', setup='pass'):
        self._stmt = stmt
        self._setup = setup

    @property
    def stmt(self):
        return self._stmt

    @property
    def setup(self):
        return self._setup


class TimeitResult(object):
    '''This class stores a result of Timeit.

    Args:
        loops (int): Number of loops done per measurement.
        repeat (int): Number of times the measurement has been repeated.
        all_runs (list(float)): Execution time of each run (in seconds).
        precision: number of significant digits.
    '''
    def __init__(self, *, loops, repeat, all_runs, precision=3):
        self._loops = loops
        self._repeat = repeat
        self._best = min(all_runs) / loops
        self._worst = max(all_runs) / loops

        timings = [dt / loops for dt in all_runs]
        self._average = math.fsum(timings) / len(timings)
        self._stdev = math.sqrt(math.fsum([(x - self._average) ** 2 for x in timings]) / len(timings))

        self._precision = precision

    @property
    def loops(self):
        return self._loops

    @property
    def repeat(self):
        return self._repeat

    @property
    def best(self):
        return self._best

    @property
    def worst(self):
        return self._worst

    @property
    def average(self):
        return self._average

    @property
    def stdev(self):
        return self._stdev

    def is_reliable(self):
        return self._worst < self._best * 4

    def warning_message(self):
        if self.is_reliable():
            return ''

        fmt = 'The test results are likely unreliable.\n' \
              'The worst time {worst} was more than four times slower than the best time {best}.'

        return fmt.format(
            worst=_format_time(timespan=self._worst, precision=self._precision),
            best=_format_time(timespan=self._best, precision=self._precision)
        )

    def report_standard_info(self):
        '''Reports standard information.'''
        fmt = '{loops} loops, best of {runs}: {best} per loop'
        return fmt.format(
            loops=self.loops,
            runs=self.repeat,
            best=_format_time(timespan=self.best, precision=self._precision)
        )

    def report_statistical_info(self):
        '''Reports statistical information.'''
        fmt = '{mean} {pm} {stdev} per loop (mean {pm} s.d. of {runs} run{run_plural}, {loops} loop{loop_plural} each)'
        return fmt.format(
            mean=_format_time(timespan=self.average, precision=self._precision),
            pm='\xb1',
            stdev=_format_time(timespan=self.stdev, precision=self._precision),
            runs=self.repeat,
            run_plural='s' if self.repeat > 1 else '',
            loops=self.loops,
            loop_plural='s' if self.loops > 1 else ''
        )


def _seconds_to_hrf(seconds, *, separator=' '):
    '''Convert seconds to human readable format.

    Args:
        seconds (int): seconds to convert.
        separator (str): separator.

    Returns:
        str: Human readable format.
    '''
    parts = [
        ('w', 60 * 60 * 24 * 7),
        ('d', 60 * 60 * 24),
        ('h', 60 * 60),
        ('m', 60),
        ('s', 1)
    ]

    time = []
    leftover = seconds
    for suffix, length in parts:
        value = int(leftover / length)
        if value > 0:
            leftover %= length
            time.append('{}{}'.format(str(value), suffix))
        if leftover < 1:
            break

    return separator.join(time)


def _format_time(timespan, precision=3):
    if timespan > 60.0:
        return _seconds_to_hrf(timespan)

    units = ('s', 'ms', '\xb5s', 'ns')
    scaling = (1, 1e+3, 1e+6, 1e+9)
    if timespan > 0.0:
        order = min(max(-int(math.floor(math.log10(timespan)) // 3), 0), 3)
    else:
        order = 3

    return '{0:.{1}g} {2}'.format(timespan * scaling[order], precision, units[order])


def _autorange(timer, is_ns_timer=False):
    '''Return the number of loops so that total time >= 0.2.'''
    THRESHOLD = int(0.2 * 1.0e+9) if is_ns_timer else 0.2
    i = 1
    while True:
        for j in 1, 2, 5:
            number = i * j
            time_taken = timer.timeit(number=number)
            if time_taken >= THRESHOLD:
                return number
        i *= 10


def bench(
        datasets,
        dataset_sizes,
        kernels,
        repeat=0,
        number=0,
        disable_tqdm=False,
        enable_validation=True,
        force_gc=True
):
    '''Core process.

    Args:
        datasets (list(:class:`Dataset`)):
        dataset_sizes (list(int)):
        kernels (list(:class:`Kernel`)):
        repeat (int): Number of times the measurement is repeated.
            When zero, this value is determined automatically.
        number (int): Number of loops to execute per measurement.
            When zero, this value is determined automatically.
        disable_tqdm (bool):
        enable_validation (bool):
        force_gc (bool): True if force garbage collection immediately
            after generating data False otherwise.

    Returns:
        Benchmark results.
    '''
    if enable_validation:
        validate(
            datasets=datasets,
            dataset_sizes=dataset_sizes,
            kernels=kernels,
            repeat=repeat,
            number=number
        )

    # select a performance counter.
    try:
        timer = time.perf_counter_ns  # python >= 3.7
        is_ns_timer = True
    except AttributeError:
        timer = time.perf_counter
        is_ns_timer = False

    if repeat == 0:
        default_repeat = 7 if timeit.default_repeat < 7 else timeit.default_repeat
        repeat = default_repeat

    shape = (len(kernels), len(datasets))
    res = utils.create_empty_array_of_shape(shape)
    for i, j in itertools.product(range(shape[0]), range(shape[1])):
        res[i][j] = []

    globals().update({'DATASET': None, 'EXTRA_ARGS': None})
    global DATASET, EXTRA_ARGS
    SETUP = 'from {} import DATASET, EXTRA_ARGS'.format(__name__)

    for i, dataset in enumerate(tqdm(datasets, disable=disable_tqdm)):
        has_multiple = len(dataset.factories) > 1
        EXTRA_ARGS = dataset.extra_args

        for j, dataset_size in enumerate(tqdm(dataset_sizes, disable=disable_tqdm)):
            if has_multiple:
                data_gen = (factory(dataset_size) for factory in dataset.factories)
            else:
                DATASET = dataset.factories[0](dataset_size)
                if force_gc:
                    gc.collect()

            for k, kernel in enumerate(kernels):
                if has_multiple:
                    DATASET = next(data_gen)
                    if force_gc:
                        gc.collect()

                setup = SETUP + '\n' + kernel.setup
                t = timeit.Timer(stmt=kernel.stmt, setup=setup, timer=timer)

                loops = number if number > 0 else _autorange(timer=t, is_ns_timer=is_ns_timer)
                all_runs = t.repeat(repeat=repeat, number=loops)
                if is_ns_timer:
                    all_runs = [value * 1.0e-9 for value in all_runs]

                res[k][i].append(
                    TimeitResult(
                        loops=loops,
                        repeat=repeat,
                        all_runs=all_runs,
                        precision=4
                    )
                )

    globals().pop('DATASET', None)
    globals().pop('EXTRA_ARGS', None)

    return res
