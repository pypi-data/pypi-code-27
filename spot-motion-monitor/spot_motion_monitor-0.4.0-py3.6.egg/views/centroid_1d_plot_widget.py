#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import numpy as np
from pyqtgraph import GraphicsLayoutWidget

__all__ = ['Centroid1dPlotWidget']

class Centroid1dPlotWidget(GraphicsLayoutWidget):

    """This class handles managing the centroid plots for both x and y
       coordinates.

    Attributes
    ----------
    curve : pyqtgraph.PlotItem
        Instance of the line plot.
    data : numpy.array
        Container for the centroid data.
    dataCounter : int
        Number of times data array has been appended to up until array size.
    dataSize : int
        The requested size of the data array.
    roiFps : float
        The camera ROI FPS.
    rollArray : bool
        Flag as to when to start rolling the data array of centroid values.
    """

    def __init__(self, parent=None):
        """Initialize the class.

        Parameters
        ----------
        parent : None, optional
            Top-level widget.
        """
        super().__init__(parent)
        self.curve = None
        self.dataSize = None
        self.data = None
        self.timeRange = None
        self.rollArray = False
        self.dataCounter = 0
        self.roiFps = None

    def setup(self, arraySize, axisLabel, roiFps):
        """Provide information for setting up the plot.

        Parameters
        ----------
        arraySize : int
            The size for the plot data array.
        axisLabel : str
            The label for the axis.
        roiFps : float
            The camera ROI FPS.
        """
        self.dataSize = arraySize
        self.data = np.array([])
        self.timeRange = np.array([])
        self.roiFps = roiFps
        p1 = self.addPlot()
        self.curve = p1.plot(self.data)
        p1.setLabel('bottom', 'Time', units='s')
        p1.setLabel('left', axisLabel, units='pixel')

    def updatePlot(self, centroid):
        """Update the plot with a new centroid.

        Parameters
        ----------
        centroid : float
            The current centroid value to plot.
        """
        if self.rollArray:
            self.data[:-1] = self.data[1:]
            self.data[-1] = centroid
        else:
            # This does create copies of arrays, so watch performance.
            self.data = np.append(self.data, centroid)
            self.timeRange = np.arange(self.data.size) / self.roiFps

        self.curve.setData(self.timeRange, self.data)
        if self.data.size > 0.1 * self.dataSize:
            self.curve.setDownsampling('mean')

        if self.dataCounter < self.dataSize:
            self.dataCounter += 1
            if self.dataCounter == self.dataSize:
                self.rollArray = True
