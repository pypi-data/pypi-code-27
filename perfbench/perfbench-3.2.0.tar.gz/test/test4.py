#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sys
sys.path.append('../')
from perfbench import *


def main():
    bm = Benchmark(
        datasets=[
            Dataset(
                factories=[
                    lambda n: np.random.uniform(low=0., high=1., size=n).astype(np.float64),  # for karnels[0]
                    lambda n: np.random.uniform(low=-1., high=0., size=n).astype(np.float64),  # for karnels[1]
                ],
                title='float64'
            ),
            Dataset(
                factories=[
                    lambda n: np.random.uniform(low=0., high=1., size=n).astype(np.float32),  # for kernels[0]
                    lambda n: np.random.uniform(low=-1., high=0., size=n).astype(np.float32),  # for kernels[1]
                ],
                title='float32'
            )
        ],
        dataset_sizes=[2 ** n for n in range(10)],
        kernels=[
            Kernel(
                stmt='np.signbit(DATASET)',
                setup='import numpy as np',
                label='signbit(pos)'
            ),
            Kernel(
                stmt='np.signbit(DATASET)',
                setup='import numpy as np',
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
