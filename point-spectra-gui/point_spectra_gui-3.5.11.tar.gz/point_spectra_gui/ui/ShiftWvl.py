# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupLayout = QtWidgets.QGroupBox(Form)
        self.groupLayout.setObjectName("groupLayout")
        self.gridLayout = QtWidgets.QGridLayout(self.groupLayout)
        self.gridLayout.setObjectName("gridLayout")
        self.choosedata = QtWidgets.QComboBox(self.groupLayout)
        self.choosedata.setObjectName("choosedata")
        self.gridLayout.addWidget(self.choosedata, 0, 1, 1, 1)
        self.choosedata_label = QtWidgets.QLabel(self.groupLayout)
        self.choosedata_label.setObjectName("choosedata_label")
        self.gridLayout.addWidget(self.choosedata_label, 0, 0, 1, 1)
        self.shifts_label = QtWidgets.QLabel(self.groupLayout)
        self.shifts_label.setObjectName("shifts_label")
        self.gridLayout.addWidget(self.shifts_label, 1, 0, 1, 1)
        self.shifts = QtWidgets.QLineEdit(self.groupLayout)
        self.shifts.setObjectName("shifts")
        self.gridLayout.addWidget(self.shifts, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.groupLayout.setTitle(("Wavelength Shift"))
        self.choosedata_label.setText(("Choose data to shift"))
        self.shifts_label.setText(("Shift amounts (comma separated)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

