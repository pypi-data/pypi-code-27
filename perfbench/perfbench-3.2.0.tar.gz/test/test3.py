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
                    lambda n: np.random.uniform(low=-1., high=1., size=n).astype(np.float64),
                ],
                title='float64 to float32',
                extra_args=dict(
                    dtype=np.float32
                )
            ),
            Dataset(
                factories=[
                    lambda n: np.random.uniform(low=-1., high=1., size=n).astype(np.float32),
                ],
                title='float32 to float16',
                extra_args=dict(
                    dtype=np.float16
                )
            )
        ],
        dataset_sizes=[2 ** n for n in range(15)],
        kernels=[
            Kernel(
                stmt="DATASET.astype(EXTRA_ARGS['dtype'])",
                label='astype'
            ),
            Kernel(
                stmt="EXTRA_ARGS['dtype'](DATASET)",
                label='dtype'
            ),
        ],
        xlabel='dataset sizes',
        title='cast',
    )
    bm.run()
    bm.plot()
    bm.save_as_html(filepath='plot3.html')
    bm.save_as_png(filepath='plot3.png')


if __name__ == '__main__':
    main()
