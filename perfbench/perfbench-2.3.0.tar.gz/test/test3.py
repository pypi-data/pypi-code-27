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
                stmts=[lambda n: np.random.uniform(low=-1., high=1., size=n).astype(np.float64), ],
                title='float64 to float32',
                extra_args=dict(
                    dtype=np.float32
                )
            ),
            Dataset(
                stmts=[lambda n: np.random.uniform(low=-1., high=1., size=n).astype(np.float32), ],
                title='float32 to float16',
                extra_args=dict(
                    dtype=np.float16
                )
            )
        ],
        dataset_sizes=[2 ** n for n in range(15)],
        kernels=[
            Kernel(
                stmt=lambda x, args: x.astype(args['dtype']),
                label='astype'
            ),
            Kernel(
                stmt=lambda x, args: args['dtype'](x),
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
