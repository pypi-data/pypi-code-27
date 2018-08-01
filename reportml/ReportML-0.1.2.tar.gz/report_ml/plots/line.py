import matplotlib.pyplot as plt
from plot_instance import PlotInstance

class LinePlot(PlotInstance):
    def __init__(self,*args):
        super(LinePlot, self).__init__(*args)

    def start(self):
        plt.plot(self.data)
