import os
import time
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

class MessageLine(QtWidgets.QWidget):
    def __init__(self, text, now, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QHBoxLayout()

        # <editor-fold desc="left side">
        self.left = QtWidgets.QWidget()
        self.left_box = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(45, 45)
        self.image_label.setScaledContents(True)
        self.path_to_standard_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\standard.png')
        self.image_label.setPixmap(QtGui.QPixmap(self.path_to_standard_image))
        self.image_label.show()


        # self.text_label = QtWidgets.QLabel(text)
        # self.text_label.setWordWrap(True)
        self.text_label = QtWidgets.QTextEdit(text)
        self.text_label.setReadOnly(True)
        self.text_label.setFrameStyle(QtWidgets.QFrame.NoFrame)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Base, QtCore.Qt.transparent)
        self.setPalette(pal)
        self.text_label.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.text_label.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)


        self.left_box.addWidget(self.image_label)
        self.left_box.addWidget(self.text_label)
        self.left_box.setAlignment(self.image_label, QtCore.Qt.AlignTop)
        self.left_box.setAlignment(self.text_label, QtCore.Qt.AlignVCenter)
        # self.left_box.addStretch()
        self.left.setLayout(self.left_box)
        # </editor-fold>

        # <editor-fold desc="right side">
        self.right = QtWidgets.QWidget()
        self.right_box = QtWidgets.QHBoxLayout()
        self.time_label = QtWidgets.QLabel(time.strftime('%H:%M', now))
        self.time_label.setMaximumWidth(45)
        self.right_box.addWidget(self.time_label)
        self.right_box.setAlignment(self.time_label, QtCore.Qt.AlignVCenter)
        self.right.setLayout(self.right_box)
        # </editor-fold>

        # <editor-fold desc="set main layout">
        self.layout.addWidget(self.left)
        self.layout.addWidget(self.right)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.setLayout(self.layout)
        # </editor-fold>


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MessageLine('hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohello',time.localtime(time.time()))
    window.show()
    sys.exit(app.exec_())