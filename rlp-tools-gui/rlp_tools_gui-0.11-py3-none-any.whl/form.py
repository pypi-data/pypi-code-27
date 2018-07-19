# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Goldstein\Desktop\rlp_tools_gui\rlp_tools_gui\form.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(810, 351)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 651, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 300, 791, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.BottomToTop)
        self.progressBar.setObjectName("progressBar")
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(10, 10, 190, 30))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(610, 10, 190, 30))
        self.pushButton2.setObjectName("pushButton2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 60, 790, 221))
        self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(210, 10, 190, 30))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton4.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.pushButton4.setObjectName("pushButton4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Инструменты переводчика DST"))
        self.pushButton1.setText(_translate("MainWindow", "Добавить строки из strings.pot"))
        self.pushButton2.setText(_translate("MainWindow", "Слить файл с  DST.po"))
        self.pushButton3.setText(_translate("MainWindow", "Сохранить строки без перевода"))
        self.pushButton4.setText(_translate("MainWindow", "Проверить структуру файла"))

