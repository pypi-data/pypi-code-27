#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import numpy as np
from scipy import ndimage

from spot_motion_monitor.utils import GenericFrameInformation

__all__ = ['RoiFrameModel']

class RoiFrameModel():

    """This class handles the calculations for a ROI CCD frame.

    The class handles all of the calculations necessary to produce information
    to fill out a GenericFrameInformation instance.

    Attributes
    ----------
    thresholdFactor : float
        Description
    """

    def __init__(self):
        """Initialize the class.
        """
        self.thresholdFactor = 0.3

    def calculateCentroid(self, roiFrame):
        """This function performs calculations for the ROI CCD frame.

        Parameters
        ----------
        roiFrame : numpy.array
            A ROI CCD frame.

        Returns
        -------
        GenericInformation
            The instance containing the results of the calculations.
        """
        newFrame = np.copy(roiFrame)
        newFrame = newFrame - self.thresholdFactor * newFrame.max()
        newFrame[newFrame < 0] = 0
        maxAdc = newFrame.max()
        flux = np.sum(newFrame)
        comX, comY = ndimage.center_of_mass(newFrame)
        objectSize = np.count_nonzero(newFrame)
        # Get standard deviation of original image without object pixels
        maxStd = np.std(np.ma.masked_array(roiFrame, mask=newFrame))
        return GenericFrameInformation(comX, comY, flux, maxAdc, objectSize, maxStd)
