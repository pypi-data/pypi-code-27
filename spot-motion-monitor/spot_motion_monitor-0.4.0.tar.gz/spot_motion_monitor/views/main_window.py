#------------------------------------------------------------------------------
# Copyright (c) 2018 LSST Systems Engineering
# Distributed under the MIT License. See LICENSE for more information.
#------------------------------------------------------------------------------
import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets

from spot_motion_monitor.controller.camera_controller import CameraController
from spot_motion_monitor.controller.data_controller import DataController
from spot_motion_monitor.controller.plot_ccd_controller import PlotCcdController
from spot_motion_monitor.controller.plot_centroid_controller import PlotCentroidController
from spot_motion_monitor.controller.plot_psd_controller import PlotPsdController
from spot_motion_monitor.views import Ui_MainWindow
from spot_motion_monitor import __version__

__all__ = ['main']

class SpotMotionMonitor(QtWidgets.QMainWindow, Ui_MainWindow):

    """This is the main application class.

    Attributes
    ----------
    cameraController : .CameraController
        An instance of the camera controller.
    plotController : .PlotCcdController
        An instance of the plot controller.
    """

    def __init__(self, parent=None):
        """Initialize the class.

        Parameters
        ----------
        parent : None, optional
            Top-level widget.
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Spot Motion Monitor")

        self.plotController = PlotCcdController(self.cameraPlot)

        self.cameraController = CameraController(self.cameraControl)
        # FIXME: Make this dynamic
        self.cameraController.setupCamera('GaussianCamera')

        self.dataController = DataController(self.cameraData)

        self.plotCentroidController = PlotCentroidController(self.centroidXPlot,
                                                             self.centroidYPlot,
                                                             self.scatterPlot)

        self.plotPsdController = PlotPsdController(self.psdXPlot, self.psdYPlot)

        bufferSize = self.dataController.getBufferSize()
        roiFps = self.cameraController.currentRoiFps()
        self.plotCentroidController.setup(bufferSize, roiFps)
        self.plotPsdController.setup(25, bufferSize / roiFps)

        self.setActionIcon(self.actionExit, "exit.svg", True)

        self.cameraController.frameTimer.timeout.connect(self.acquireFrame)
        self.cameraController.updateStatusBar.displayStatus.connect(self.updateStatusBar)
        self.plotController.updateStatusBar.displayStatus.connect(self.updateStatusBar)
        self.dataController.updateStatusBar.displayStatus.connect(self.updateStatusBar)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about)

    def about(self):
        """This function presents the about dialog box.
        """
        about = QtWidgets.QMessageBox()
        about.setIconPixmap(QtGui.QPixmap(":smm_logo_sm.png"))
        about.setWindowTitle("About the Spot Motion Monitor")
        about.setStandardButtons(QtWidgets.QMessageBox.Ok)
        about.setInformativeText('''
                                 <b>Spot Motion Monitor</b> v{}
                                 <p>
                                 This application is the front-end for a system that
                                 monitors seeing within a telescope dome.
                                 </p>
                                 <br><br>
                                 Copyright 2018 LSST Systems Engineering
                                 '''.format(__version__))
        about.exec_()

    def acquireFrame(self):
        """Handle a camera CCD frame.
        """
        frame = self.cameraController.getFrame()
        cameraStatus = self.cameraController.currentStatus()
        self.dataController.passFrame(frame, cameraStatus)
        self.plotController.passFrame(frame)
        centroids = self.dataController.getCentroids(cameraStatus.isRoiMode)
        self.plotCentroidController.update(centroids[0], centroids[1])
        psdData = self.dataController.getPsd(cameraStatus.isRoiMode, cameraStatus.currentFps)
        self.plotPsdController.update(psdData[0], psdData[1], psdData[2])

    def setActionIcon(self, action, iconName, iconInMenu=False):
        """Setup the icon for the given action.

        Parameters
        ----------
        action : QAction
          A specific program action.
        iconName : str
          Name of the icon in the QRC file.
        iconInMenu : bool, optional
          Make the icon visible in the program menu.
        """
        action.setIcon(QtGui.QIcon(QtGui.QPixmap(':{}'.format(iconName))))
        action.setIconVisibleInMenu(iconInMenu)

    def updateStatusBar(self, message, timeout):
        """This function updates the application status bar.

        Parameters
        ----------
        message : str
            The text to display in the status bar.
        timeout : int
            The time (in milliseconds) for the text to remain visible.
        """
        self.statusbar.showMessage(message, timeout)


def main():
    """
    This is the entrance point of the program
    """
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("LSST-Systems-Engineering")
    app.setOrganizationDomain("lsst.org")
    app.setApplicationName("Spot Motion Monitor")
    form = SpotMotionMonitor()
    form.show()
    app.exec_()
