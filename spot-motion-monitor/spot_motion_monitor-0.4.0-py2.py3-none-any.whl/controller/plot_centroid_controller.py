#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
__all__ = ['PlotCentroidController']

class PlotCentroidController():

    """This class handles the interactions between the main program and the
       1D centroid plots.

    Attributes
    ----------
    scatterPlot : .GraphicsLayoutWidget
        The scatter plot of the x,y pixel coordinate of the centroid.
    x1dPlot : .GraphicsLayoutWidget
        The 1D plot of the x pixel coordinate of the centroid.
    y1dPlot : .GraphicsLayoutWidget
        The 1D plot of the y pixel coordinate of the centroid.
    """

    def __init__(self, cxp, cyp, csp):
        """Initialize the class.

        Parameters
        ----------
        cxp : .GraphicsLayoutWidget
            The instance of the x centroid plot.
        cyp : .GraphicsLayoutWidget
            The instance of the y centroid plot.
        csp : .GraphicsLayoutWidget
            The instance of the centroid scatter plot.
        """
        self.x1dPlot = cxp
        self.y1dPlot = cyp
        self.scatterPlot = csp

    def setup(self, arraySize, roiFps):
        """Pass along the requested array size to the contained plot widgets.

        Parameters
        ----------
        arraySize : int
            The size for the plot data array.
        roiFps : float
            The current camera ROI frames per second.
        """
        self.x1dPlot.setup(arraySize, 'X', roiFps)
        self.y1dPlot.setup(arraySize, 'Y', roiFps)
        self.scatterPlot.setup(arraySize)

    def update(self, cx, cy):
        """Update the x and y centroid plots with current values.

        Parameters
        ----------
        cx : float
            The x pixel coordinate of the centroid.
        cy : float
            The y pixel coordinate of the centroid.
        """
        if cx is None or cy is None:
            return
        self.x1dPlot.updatePlot(cx)
        self.y1dPlot.updatePlot(cy)
        self.scatterPlot.updatePlot(cx, cy)
