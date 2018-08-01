import matplotlib.pyplot as plt
from plot_instance import PlotInstance


class HistogramPlot(PlotInstance):
    def __init__(self, *args):
        super(HistogramPlot, self).__init__(*args)

    def start(self):
        plt.hist(x=self.data)
