#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import timeit
import itertools
from . import utils
from . import ipython_utils


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
        title (str):
    '''
    def __init__(self, factories, *, extra_args=None, title=None):
        self._factories = factories
        self._extra_args = extra_args
        self._title = '' if title is None else title

    @property
    def factories(self):
        return self._factories

    @property
    def extra_args(self):
        return self._extra_args

    @property
    def title(self):
        return self._title


class Kernel(object):
    '''Kernel class.

    Args:
        stmt:
        setup:
        label (str):
    '''
    def __init__(self, stmt='pass', setup='pass', label=None):
        self._stmt = stmt
        self._setup = setup
        self._label = '' if label is None else label

    @property
    def stmt(self):
        return self._stmt

    @property
    def setup(self):
        return self._setup

    @property
    def label(self):
        return self._label


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
        disable_tqdm=False
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

    Returns:
        Benchmark results.
    '''
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

            for k, kernel in enumerate(kernels):
                if has_multiple:
                    DATASET = next(data_gen)

                setup = SETUP + '\n' + kernel.setup
                t = timeit.Timer(stmt=kernel.stmt, setup=setup, timer=timer)

                loops = number if number > 0 else _autorange(timer=t, is_ns_timer=is_ns_timer)
                all_runs = t.repeat(repeat=repeat, number=loops)
                if is_ns_timer:
                    all_runs = [value * 1.0e-9 for value in all_runs]

                res[k][i].append(
                    ipython_utils.TimeitResult(
                        loops=loops,
                        repeat=repeat,
                        all_runs=all_runs,
                        precision=4
                    )
                )

    globals().pop('DATASET', None)
    globals().pop('EXTRA_ARGS', None)

    return res
