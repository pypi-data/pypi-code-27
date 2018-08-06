# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'galacteek/ui/donatedialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DonateDialog(object):
    def setupUi(self, DonateDialog):
        DonateDialog.setObjectName("DonateDialog")
        DonateDialog.resize(875, 293)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DonateDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(DonateDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 200))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.label = QtWidgets.QLabel(DonateDialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.moneroAddress = QtWidgets.QLabel(DonateDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.moneroAddress.setFont(font)
        self.moneroAddress.setText("")
        self.moneroAddress.setTextFormat(QtCore.Qt.RichText)
        self.moneroAddress.setWordWrap(False)
        self.moneroAddress.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.moneroAddress.setObjectName("moneroAddress")
        self.horizontalLayout.addWidget(self.moneroAddress)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.moneroClip = QtWidgets.QPushButton(DonateDialog)
        self.moneroClip.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/share/icons/clipboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moneroClip.setIcon(icon)
        self.moneroClip.setObjectName("moneroClip")
        self.horizontalLayout.addWidget(self.moneroClip)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_3 = QtWidgets.QLabel(DonateDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bitcoinAddress = QtWidgets.QLabel(DonateDialog)
        self.bitcoinAddress.setText("")
        self.bitcoinAddress.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.bitcoinAddress.setObjectName("bitcoinAddress")
        self.horizontalLayout_2.addWidget(self.bitcoinAddress)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.bitcoinClip = QtWidgets.QPushButton(DonateDialog)
        self.bitcoinClip.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.bitcoinClip.setText("")
        self.bitcoinClip.setIcon(icon)
        self.bitcoinClip.setObjectName("bitcoinClip")
        self.horizontalLayout_2.addWidget(self.bitcoinClip)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.okButton = QtWidgets.QPushButton(DonateDialog)
        self.okButton.setMinimumSize(QtCore.QSize(200, 0))
        self.okButton.setObjectName("okButton")
        self.verticalLayout_2.addWidget(self.okButton, 0, QtCore.Qt.AlignRight)

        self.retranslateUi(DonateDialog)
        QtCore.QMetaObject.connectSlotsByName(DonateDialog)

    def retranslateUi(self, DonateDialog):
        _translate = QtCore.QCoreApplication.translate
        DonateDialog.setWindowTitle(_translate("DonateDialog", "Dialog"))
        self.textBrowser.setHtml(_translate("DonateDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Any donation is most welcome to help keep the project\'s development going. The application\'s translation to other languages is planned as well as new features. Donations will help support other projects like </span><a href=\"https://ipfs-search.com\"><span style=\" text-decoration: underline; color:#0000ff;\">IPFS Search</span></a></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">You can make a donation with Monero (or bitcoin) using the addresses below.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Thanks!</span></p></body></html>"))
        self.label.setText(_translate("DonateDialog", "Monero donation address"))
        self.label_3.setText(_translate("DonateDialog", "Bitcoin donation address"))
        self.okButton.setText(_translate("DonateDialog", "OK"))

from . import galacteek_rc
