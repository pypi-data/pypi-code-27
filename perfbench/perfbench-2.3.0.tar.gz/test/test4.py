#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append('../')
from perfbench.process import *


def main():
    bm = Benchmark(
        datasets=[
            Dataset(
                stmts=[
                    lambda n: np.random.uniform(low=0., high=1., size=n).astype(np.float64),  # for karnels[0]
                    lambda n: np.random.uniform(low=-1., high=0., size=n).astype(np.float64),  # for karnels[1]
                ],
                title='float64'
            ),
            Dataset(
                stmts=[
                    lambda n: np.random.uniform(low=0., high=1., size=n).astype(np.float32),  # for kernels[0]
                    lambda n: np.random.uniform(low=-1., high=0., size=n).astype(np.float32),  # for kernels[1]
                ],
                title='float32'
            )
        ],
        dataset_sizes=[2 ** n for n in range(15)],
        kernels=[
            Kernel(
                stmt=lambda x: np.signbit(x),
                label='signbit(pos)'
            ),
            Kernel(
                stmt=lambda x: np.signbit(x),
                label='signbit(neg)'
            ),
        ],
        xlabel='dataset sizes',
        title='signbit',
    )
    bm.run()
    bm.plot()
    bm.save_as_html(filepath='plot4.html')
    bm.save_as_png(filepath='plot4.png')


if __name__ == '__main__':
    main()
