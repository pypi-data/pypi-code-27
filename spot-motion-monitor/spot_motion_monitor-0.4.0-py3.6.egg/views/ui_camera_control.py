# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms/camera_control.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CameraControl(object):
    def setupUi(self, CameraControl):
        CameraControl.setObjectName("CameraControl")
        CameraControl.resize(192, 229)
        CameraControl.setMinimumSize(QtCore.QSize(190, 110))
        self.verticalLayout = QtWidgets.QVBoxLayout(CameraControl)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.startStopButton = QtWidgets.QPushButton(CameraControl)
        self.startStopButton.setCheckable(True)
        self.startStopButton.setObjectName("startStopButton")
        self.verticalLayout.addWidget(self.startStopButton)
        self.acquireFramesButton = QtWidgets.QPushButton(CameraControl)
        self.acquireFramesButton.setCheckable(True)
        self.acquireFramesButton.setObjectName("acquireFramesButton")
        self.verticalLayout.addWidget(self.acquireFramesButton)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.acquireRoiCheckBox = QtWidgets.QCheckBox(CameraControl)
        self.acquireRoiCheckBox.setObjectName("acquireRoiCheckBox")
        self.horizontalLayout.addWidget(self.acquireRoiCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(CameraControl)
        QtCore.QMetaObject.connectSlotsByName(CameraControl)

    def retranslateUi(self, CameraControl):
        _translate = QtCore.QCoreApplication.translate
        CameraControl.setWindowTitle(_translate("CameraControl", "Form"))
        self.startStopButton.setText(_translate("CameraControl", "Start Camera"))
        self.acquireFramesButton.setText(_translate("CameraControl", "Start Acquire Frames"))
        self.acquireRoiCheckBox.setText(_translate("CameraControl", "Acquire ROI"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CameraControl = QtWidgets.QWidget()
    ui = Ui_CameraControl()
    ui.setupUi(CameraControl)
    CameraControl.show()
    sys.exit(app.exec_())

