import matplotlib.pyplot as plt
from plot import Plot
class PlotInstance(object):
    def __init__(self,data,title, xlabel=None, ylabel=None):
        """
        Initialize a plot instance
        :param data: the raw y axis data of the items to be placed in a histogram
        :param title: the title to give the histogram
        :param xlabel: xlabel of the plot
        :param ylabel: the ylabel of the plot
        """
        self.data = data
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def render(self):
        self.start()
        plt.title(self.title)
        plt.ylabel(self.ylabel)
        plt.xlabel(self.ylabel)
        return Plot(self.title,plt)

    def start(self):
        pass
