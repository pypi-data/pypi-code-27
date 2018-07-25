# -*- coding: utf-8 -*-

# Automatically generated - don't edit.
# Use `python setup.py build_ui` to update it.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.filebrowse = QtWidgets.QPushButton(self.groupBox)
        self.filebrowse.setMaximumSize(QtCore.QSize(30, 16777215))
        self.filebrowse.setObjectName("filebrowse")
        self.gridLayout.addWidget(self.filebrowse, 1, 1, 1, 1)
        self.lookupfile = QtWidgets.QLineEdit(self.groupBox)
        self.lookupfile.setFrame(True)
        self.lookupfile.setReadOnly(True)
        self.lookupfile.setObjectName("lookupfile")
        self.gridLayout.addWidget(self.lookupfile, 1, 0, 1, 1)
        self.choosedata = QtWidgets.QComboBox(self.groupBox)
        self.choosedata.setObjectName("choosedata")
        self.gridLayout.addWidget(self.choosedata, 0, 0, 1, 1)
        self.right_on = QtWidgets.QComboBox(self.groupBox)
        self.right_on.setObjectName("right_on")
        self.gridLayout.addWidget(self.right_on, 1, 2, 1, 1)
        self.left_on = QtWidgets.QComboBox(self.groupBox)
        self.left_on.setObjectName("left_on")
        self.gridLayout.addWidget(self.left_on, 0, 2, 1, 1)
        self.skiprows_label = QtWidgets.QLabel(self.groupBox)
        self.skiprows_label.setObjectName("skiprows_label")
        self.gridLayout.addWidget(self.skiprows_label, 3, 0, 1, 1)
        self.skiprows_spin = QtWidgets.QSpinBox(self.groupBox)
        self.skiprows_spin.setObjectName("skiprows_spin")
        self.gridLayout.addWidget(self.skiprows_spin, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(("Form"))
        self.groupBox.setTitle(("Look Up Metadata"))
        self.filebrowse.setText(("..."))
        self.skiprows_label.setText(("# of rows to skip"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

