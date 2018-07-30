#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
from PyQt5.QtCore import Qt

from spot_motion_monitor.controller.camera_controller import CameraController
from spot_motion_monitor.utils import ONE_SECOND_IN_MILLISECONDS
from spot_motion_monitor.views.camera_control_widget import CameraControlWidget

class TestCameraController():

    def test_parametersAfterConstruction(self, qtbot):
        ccWidget = CameraControlWidget()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        assert cc.cameraControlWidget is not None
        assert cc.camera is None
        assert cc.frameTimer is not None
        assert cc.updateStatusBar is not None

    def test_cameraObject(self, qtbot):
        ccWidget = CameraControlWidget()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        assert cc.camera is not None
        assert hasattr(cc.camera, "seed")

    def test_cameraStartStop(self, qtbot, mocker):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        mocker.patch('spot_motion_monitor.camera.gaussian_camera.GaussianCamera.startup')
        qtbot.mouseClick(ccWidget.startStopButton, Qt.LeftButton)
        assert cc.camera.startup.call_count == 1
        mocker.patch('spot_motion_monitor.camera.gaussian_camera.GaussianCamera.shutdown')
        qtbot.mouseClick(ccWidget.startStopButton, Qt.LeftButton)
        assert cc.camera.shutdown.call_count == 1

    def test_cameraAcquireFrames(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        qtbot.mouseClick(ccWidget.acquireFramesButton, Qt.LeftButton)
        assert cc.frameTimer.isActive()
        interval = int((1 / cc.currentCameraFps()) * ONE_SECOND_IN_MILLISECONDS)
        assert cc.frameTimer.interval() == interval
        qtbot.mouseClick(ccWidget.acquireFramesButton, Qt.LeftButton)
        assert not cc.frameTimer.isActive()

    def test_cameraCurrentFps(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        fps = cc.currentCameraFps()
        assert fps == 24
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        fps = cc.currentCameraFps()
        assert fps == 40

    def test_cameraAcquireRoiFrames(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        qtbot.mouseClick(ccWidget.acquireFramesButton, Qt.LeftButton)
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        interval = int((1 / cc.currentCameraFps()) * ONE_SECOND_IN_MILLISECONDS)
        assert cc.frameTimer.interval() == interval
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        interval = int((1 / cc.currentCameraFps()) * ONE_SECOND_IN_MILLISECONDS)
        assert cc.frameTimer.interval() == interval
        qtbot.mouseClick(ccWidget.acquireFramesButton, Qt.LeftButton)

    def test_cameraAcquireExpectedFrame(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        frame = cc.getFrame()
        assert frame.shape == (480, 640)
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        frame = cc.getFrame()
        assert frame.shape == (50, 50)

    def test_isRoiMode(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        isRoiMode = cc.isRoiMode()
        assert isRoiMode is False
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        isRoiMode = cc.isRoiMode()
        assert isRoiMode is True

    def test_currentOffset(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.camera.seed = 1000
        cc.startStopCamera(True)
        offset = cc.currentOffset()
        assert offset == (264, 200)

    def test_currentStatus(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.camera.seed = 1000
        cc.startStopCamera(True)
        status = cc.currentStatus()
        assert status.currentFps == 24
        assert status.isRoiMode is False
        assert status.frameOffset == (264, 200)
        qtbot.mouseClick(ccWidget.acquireRoiCheckBox, Qt.LeftButton)
        status = cc.currentStatus()
        assert status.currentFps == 40
        assert status.isRoiMode is True
        assert status.frameOffset == (264, 200)

    def test_currentRoiFps(self, qtbot):
        ccWidget = CameraControlWidget()
        ccWidget.show()
        qtbot.addWidget(ccWidget)
        cc = CameraController(ccWidget)
        cc.setupCamera("GaussianCamera")
        cc.startStopCamera(True)
        roiFps = cc.currentRoiFps()
        assert roiFps == 40
