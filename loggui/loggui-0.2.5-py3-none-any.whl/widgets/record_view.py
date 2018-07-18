from PySide2.QtWidgets import QDialog, QFormLayout, QLabel
from PySide2.QtCore import Qt
from datetime import datetime

class LogRecordDialog(QDialog):
    def __init__(self, record):
        QDialog.__init__(self)
        self.layout = QFormLayout()
        self.setWindowTitle("Log Record information")
        record = {
            "Module name":record.name,
            "Module":record.module,
            "Level name":record.levelname,
            "Level #":record.levelno,
            "Path":record.pathname,
            "Line #": record.lineno,
            "Message": record.getMessage(),
            "Time":datetime.fromtimestamp(record.created),
            "Exception Info": record.exc_info,
            "Exception Text": record.exc_text,
            "Function name": record.funcName,
            "Stack information": record.stack_info,
            "Thread name": record.threadName,
            "Process": "%s (%s)" % (record.processName, record.process)
        }
        for k, v in record.items():
            label = QLabel(str(v))
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.layout.addRow(k + ":", label)
        self.setLayout(self.layout)
