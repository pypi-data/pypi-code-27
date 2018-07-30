#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
_all__ = ['BaseCamera']

class BaseCamera():
    """Base API for all Camera classes

    Attributes
    ----------
    fpsFullFrame : int
        The Frames per Second rate in full frame mode.
    fpsRoiFrame : int
        The Frames per Second rate in ROI frame mode.
    height : int
        The height in pixels of the camera CCD
    roiSize : int
        The size of a (square) ROI region in pixels.
    width : int
        The width in pixels of the camera CCD
    """

    height = None
    width = None
    fpsFullFrame = None
    fpsRoiFrame = None
    roiSize = None

    def __init__(self):
        """Initialize the class.
        """
        pass

    def getFullFrame(self):
        """Return a full CCD frame from the camera.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def getRoiFrame(self):
        """Return a ROI CCD frame from the camera.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def shutdown(self):
        """Shutdown the camera safely.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

    def startup(self):
        """Startup the camera.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
