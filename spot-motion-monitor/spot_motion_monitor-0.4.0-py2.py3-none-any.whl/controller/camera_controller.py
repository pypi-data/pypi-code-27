#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from PyQt5.QtCore import QTimer

import spot_motion_monitor.camera
import spot_motion_monitor.utils as smmUtils

__all__ = ["CameraController"]

class CameraController():

    """This class manages the interactions between the CameraControlWidget and
       a particular instance of a BaseCamera.

    Attributes
    ----------
    camera : .BaseCamera
        A particular concrete instance of a camera.
    cameraControlWidget : .CameraControlWidget
        The instance of the camera control widget.
    """

    def __init__(self, ccw):
        """Initialize the class.

        Parameters
        ----------
        ccw : .CameraControlWidget
            An instance of the camera control widget
        """
        self.cameraControlWidget = ccw
        self.camera = None
        self.updateStatusBar = smmUtils.StatusBarUpdater()
        self.frameTimer = QTimer()

        self.cameraControlWidget.cameraState.connect(self.startStopCamera)
        self.cameraControlWidget.acquireFramesState.connect(self.acquireFrame)
        self.cameraControlWidget.acquireRoiState.connect(self.acquireRoiFrame)

    def acquireFrame(self, state):
        """Start or stop the timer for full frame acquisition.

        Parameters
        ----------
        state : bool
            The current state of the Start Frame Acquisition button.
        """
        if state:
            self.updateStatusBar.displayStatus.emit('Starting Frame Acquisition',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            if self.frameTimer.isActive():
                self.frameTimer.stop()
            current_fps = self.currentCameraFps()
            fps = current_fps if current_fps is not None else smmUtils.DEFAULT_FPS
            self.frameTimer.start(smmUtils.ONE_SECOND_IN_MILLISECONDS / fps)
        else:
            self.updateStatusBar.displayStatus.emit('Stopping Frame Acquistion',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            self.frameTimer.stop()

    def acquireRoiFrame(self, state):
        """Start or stop the timer for ROI frame acquisition.

        Parameters
        ----------
        state : bool
            The current state of the Acquire ROI checkbox.
        """
        if state:
            if self.frameTimer.isActive():
                self.frameTimer.stop()
            self.updateStatusBar.displayStatus.emit('Starting ROI Frame Acquistion',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            current_fps = self.currentCameraFps()
            fps = current_fps if current_fps is not None else smmUtils.DEFAULT_FPS
            self.frameTimer.start(smmUtils.ONE_SECOND_IN_MILLISECONDS / fps)
        else:
            self.frameTimer.stop()
            self.updateStatusBar.displayStatus.emit('Stopping ROI Frame Acquistion',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            if self.cameraControlWidget.acquireFramesButton.isChecked():
                self.acquireFrame(True)

    def currentCameraFps(self):
        """Get the current camera FPS.

        Returns
        -------
        int
            Get the current camera FPS based on the acquisition mode.
        """
        if self.cameraControlWidget.acquireRoiCheckBox.isChecked():
            return self.camera.fpsRoiFrame
        else:
            return self.camera.fpsFullFrame

    def currentOffset(self):
        """The current frame offset for the CCD.

        Returns
        -------
        (float, float)
            The x, y pixel coordinated of the current frame offset.
        """
        return self.camera.getOffset()

    def currentRoiFps(self):
        """The current camera ROI FPS.

        Returns
        -------
        float
            Get the current camera ROI FPS.
        """
        return self.camera.fpsRoiFrame

    def currentStatus(self):
        """The current status of the camera.

        Returns
        -------
        .CameraStatus
            The instance containing all of the current camera status.
        """
        fps = self.currentCameraFps()
        mode = self.isRoiMode()
        offset = self.currentOffset()
        return spot_motion_monitor.camera.CameraStatus(fps, mode, offset)

    def getFrame(self):
        """Get the frame from the camera.

        Returns
        -------
        numpy.array
            A frame from a camera CCD.
        """
        if self.cameraControlWidget.acquireRoiCheckBox.isChecked():
            return self.camera.getRoiFrame()
        else:
            return self.camera.getFullFrame()

    def isRoiMode(self):
        """The current acquisition mode.

        Returns
        -------
        bool
            True if in ROI mode, False if in full frame mode.
        """
        return self.cameraControlWidget.acquireRoiCheckBox.isChecked()

    def setupCamera(self, cameraStr):
        """Create a specific concrete instance of a camera.

        Parameters
        ----------
        cameraStr : str
            Class name for concrete camera instance.
        """
        self.camera = getattr(spot_motion_monitor.camera, cameraStr)()

    def startStopCamera(self, state):
        """Start or stop the camera.

        Parameters
        ----------
        state : bool
            The current state of the camera.
        """
        if state:
            self.updateStatusBar.displayStatus.emit('Starting Camera',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            self.camera.startup()
            self.updateStatusBar.displayStatus.emit('Camera Started Successfully',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
        else:
            self.updateStatusBar.displayStatus.emit('Stopping Camera',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
            self.camera.shutdown()
            self.updateStatusBar.displayStatus.emit('Camera Stopped Successfully',
                                                    smmUtils.ONE_SECOND_IN_MILLISECONDS)
