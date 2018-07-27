import os

import numpy as np

from hwaves import hwf_plot

tests_path = os.path.join(os.getcwd(),'tests')

nr = 60
dr = 0.2
r_max = (nr-1)*dr
r_A = np.arange(0,r_max,dr)

def test_radial_wf_plot():
    fig = hwf_plot.plot_radial_wf(1,0,r_A,showplot=False)
    fpath = os.path.join(tests_path,'radial_wf_test.png')
    fig.savefig(fpath)
    #assert(os.path.exists(fpath))


