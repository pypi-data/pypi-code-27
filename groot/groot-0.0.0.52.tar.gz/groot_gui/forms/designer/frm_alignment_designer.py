# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/martinrusilowicz/work/apps/groot/groot_gui/forms/designer/frm_alignment_designer.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def __init__(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(948, 671)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setSpacing(8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.FRA_TOOLBAR = QtWidgets.QFrame(Dialog)
        self.FRA_TOOLBAR.setObjectName("FRA_TOOLBAR")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.FRA_TOOLBAR)
        self.horizontalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LBL_POSITION_START = QtWidgets.QLabel(self.FRA_TOOLBAR)
        self.LBL_POSITION_START.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LBL_POSITION_START.setObjectName("LBL_POSITION_START")
        self.gridLayout_2.addWidget(self.LBL_POSITION_START, 1, 0, 1, 1)
        self.SCR_MAIN = QtWidgets.QScrollBar(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SCR_MAIN.sizePolicy().hasHeightForWidth())
        self.SCR_MAIN.setSizePolicy(sizePolicy)
        self.SCR_MAIN.setOrientation(QtCore.Qt.Horizontal)
        self.SCR_MAIN.setObjectName("SCR_MAIN")
        self.gridLayout_2.addWidget(self.SCR_MAIN, 1, 1, 1, 1)
        self.LBL_POSITION_END = QtWidgets.QLabel(self.FRA_TOOLBAR)
        self.LBL_POSITION_END.setObjectName("LBL_POSITION_END")
        self.gridLayout_2.addWidget(self.LBL_POSITION_END, 1, 2, 1, 1)
        self.LBL_POSITION_START_2 = QtWidgets.QLabel(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBL_POSITION_START_2.sizePolicy().hasHeightForWidth())
        self.LBL_POSITION_START_2.setSizePolicy(sizePolicy)
        self.LBL_POSITION_START_2.setObjectName("LBL_POSITION_START_2")
        self.gridLayout_2.addWidget(self.LBL_POSITION_START_2, 0, 0, 1, 1)
        self.LBL_POSITION_START_3 = QtWidgets.QLabel(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBL_POSITION_START_3.sizePolicy().hasHeightForWidth())
        self.LBL_POSITION_START_3.setSizePolicy(sizePolicy)
        self.LBL_POSITION_START_3.setObjectName("LBL_POSITION_START_3")
        self.gridLayout_2.addWidget(self.LBL_POSITION_START_3, 0, 2, 1, 1)
        self.LBL_SCRPOS = QtWidgets.QLabel(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LBL_SCRPOS.sizePolicy().hasHeightForWidth())
        self.LBL_SCRPOS.setSizePolicy(sizePolicy)
        self.LBL_SCRPOS.setAlignment(QtCore.Qt.AlignCenter)
        self.LBL_SCRPOS.setObjectName("LBL_SCRPOS")
        self.gridLayout_2.addWidget(self.LBL_SCRPOS, 0, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_2)
        self.BTN_VIEW_ELSEWHERE = QtWidgets.QToolButton(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_VIEW_ELSEWHERE.sizePolicy().hasHeightForWidth())
        self.BTN_VIEW_ELSEWHERE.setSizePolicy(sizePolicy)
        self.BTN_VIEW_ELSEWHERE.setMinimumSize(QtCore.QSize(64, 64))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/groot/view.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_VIEW_ELSEWHERE.setIcon(icon)
        self.BTN_VIEW_ELSEWHERE.setIconSize(QtCore.QSize(32, 32))
        self.BTN_VIEW_ELSEWHERE.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.BTN_VIEW_ELSEWHERE.setObjectName("BTN_VIEW_ELSEWHERE")
        self.horizontalLayout_3.addWidget(self.BTN_VIEW_ELSEWHERE)
        self.BTN_REFRESH = QtWidgets.QToolButton(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_REFRESH.sizePolicy().hasHeightForWidth())
        self.BTN_REFRESH.setSizePolicy(sizePolicy)
        self.BTN_REFRESH.setMinimumSize(QtCore.QSize(64, 64))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/groot/refresh.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_REFRESH.setIcon(icon1)
        self.BTN_REFRESH.setIconSize(QtCore.QSize(32, 32))
        self.BTN_REFRESH.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.BTN_REFRESH.setObjectName("BTN_REFRESH")
        self.horizontalLayout_3.addWidget(self.BTN_REFRESH)
        self.BTN_HELP = QtWidgets.QToolButton(self.FRA_TOOLBAR)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_HELP.sizePolicy().hasHeightForWidth())
        self.BTN_HELP.setSizePolicy(sizePolicy)
        self.BTN_HELP.setMinimumSize(QtCore.QSize(64, 64))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/groot/help.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_HELP.setIcon(icon2)
        self.BTN_HELP.setIconSize(QtCore.QSize(32, 32))
        self.BTN_HELP.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.BTN_HELP.setObjectName("BTN_HELP")
        self.horizontalLayout_3.addWidget(self.BTN_HELP)
        self.verticalLayout.addWidget(self.FRA_TOOLBAR)
        self.LBL_SELECTION_WARNING = QtWidgets.QLabel(Dialog)
        self.LBL_SELECTION_WARNING.setObjectName("LBL_SELECTION_WARNING")
        self.verticalLayout.addWidget(self.LBL_SELECTION_WARNING)
        self.LBL_ERROR = QtWidgets.QLabel(Dialog)
        self.LBL_ERROR.setObjectName("LBL_ERROR")
        self.verticalLayout.addWidget(self.LBL_ERROR)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 930, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.GRID_MAIN = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.GRID_MAIN.setContentsMargins(0, 0, 0, 0)
        self.GRID_MAIN.setSpacing(0)
        self.GRID_MAIN.setObjectName("GRID_MAIN")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.LBL_INFO_5 = QtWidgets.QLabel(self.frame_2)
        self.LBL_INFO_5.setObjectName("LBL_INFO_5")
        self.gridLayout.addWidget(self.LBL_INFO_5, 0, 2, 1, 1)
        self.LBL_INFO_3 = QtWidgets.QLabel(self.frame_2)
        self.LBL_INFO_3.setObjectName("LBL_INFO_3")
        self.gridLayout.addWidget(self.LBL_INFO_3, 0, 1, 1, 1)
        self.LBL_INFO_2 = QtWidgets.QLabel(self.frame_2)
        self.LBL_INFO_2.setObjectName("LBL_INFO_2")
        self.gridLayout.addWidget(self.LBL_INFO_2, 0, 0, 1, 1)
        self.BTN_SEQUENCE = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_SEQUENCE.sizePolicy().hasHeightForWidth())
        self.BTN_SEQUENCE.setSizePolicy(sizePolicy)
        self.BTN_SEQUENCE.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/groot/black_gene.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SEQUENCE.setIcon(icon3)
        self.BTN_SEQUENCE.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SEQUENCE.setObjectName("BTN_SEQUENCE")
        self.gridLayout.addWidget(self.BTN_SEQUENCE, 1, 0, 1, 1)
        self.BTN_POSITION = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_POSITION.sizePolicy().hasHeightForWidth())
        self.BTN_POSITION.setSizePolicy(sizePolicy)
        self.BTN_POSITION.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/groot/black_domain.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_POSITION.setIcon(icon4)
        self.BTN_POSITION.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_POSITION.setObjectName("BTN_POSITION")
        self.gridLayout.addWidget(self.BTN_POSITION, 1, 1, 1, 1)
        self.BTN_SITE = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BTN_SITE.sizePolicy().hasHeightForWidth())
        self.BTN_SITE.setSizePolicy(sizePolicy)
        self.BTN_SITE.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/groot/black_alignment.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BTN_SITE.setIcon(icon5)
        self.BTN_SITE.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.BTN_SITE.setObjectName("BTN_SITE")
        self.gridLayout.addWidget(self.BTN_SITE, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.LBL_POSITION_START.setText(_translate("Dialog", "0"))
        self.LBL_POSITION_END.setText(_translate("Dialog", "0"))
        self.LBL_POSITION_START_2.setText(_translate("Dialog", "Start"))
        self.LBL_POSITION_START_3.setText(_translate("Dialog", "End"))
        self.LBL_SCRPOS.setText(_translate("Dialog", "End"))
        self.BTN_VIEW_ELSEWHERE.setText(_translate("Dialog", "View"))
        self.BTN_REFRESH.setText(_translate("Dialog", "Refresh"))
        self.BTN_HELP.setText(_translate("Dialog", "Help"))
        self.LBL_SELECTION_WARNING.setText(_translate("Dialog", "<a href=\"action:show_selection\">Select</a> a single component to view its alignment."))
        self.LBL_SELECTION_WARNING.setProperty("style", _translate("Dialog", "warning"))
        self.LBL_ERROR.setText(_translate("Dialog", "Message."))
        self.LBL_ERROR.setProperty("style", _translate("Dialog", "warning"))
        self.LBL_INFO_5.setText(_translate("Dialog", "Site"))
        self.LBL_INFO_3.setText(_translate("Dialog", "Position"))
        self.LBL_INFO_2.setText(_translate("Dialog", "Sequence"))


