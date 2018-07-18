import logging
import os
import threading
from queue import Queue
try:
    from __main__ import __file__ as mname
except ImportError:
    mname = "file name n/a"
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QHBoxLayout, QStyle
from loggui import widgets
from PySide2.QtCore import QThread, Signal
from PySide2.QtGui import QColor, QStandardItemModel, QStandardItem
from datetime import datetime
ICON_LEVELS = {
              "10":QStyle.SP_MessageBoxInformation,
              "20":QStyle.SP_MessageBoxInformation,
              "30":QStyle.SP_MessageBoxWarning,
              "40":QStyle.SP_TitleBarCloseButton,
              "50":QStyle.SP_MessageBoxCritical,
              }

LEVELS_COLOR = {
    "10":[QColor("black"), QColor("lightcyan")],
    "20":[QColor("black"), QColor("lightblue")],
    "30":[QColor("black"), QColor("yellow")],
    "40":[QColor("white"), QColor("tomato")],
    "50":[QColor("white"), QColor("darkred")]
}

class Queue2QThread(QThread):
    new_record = Signal(logging.LogRecord)

    def __init__(self, queue):
        QThread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            self.new_record.emit(self.queue.get())

class MainThreadWatcher(QThread):
    thread_stopped = Signal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while 1:
            if not threading.main_thread().is_alive():
                self.thread_stopped.emit()
                break


class _GUILog(QMainWindow):

    def __init__(self, queue, app, name):
        super().__init__()
        self.name = name
        self.app = app
        self.main_widget = QWidget()
        self.main_widget.layout = QHBoxLayout()
        # Widgets
        self.log_view = QTableView()
        self.log_sources = widgets.LogSettings()
        # Threads
        self.upd_thread = Queue2QThread(queue)
        self.main_thread_watch = MainThreadWatcher()
        self.main_thread_watch.thread_stopped.connect(self.mt_stop)
        self.upd_thread.new_record.connect(self.new_record)
        self.upd_thread.start()
        self.main_thread_watch.start()
        self.initUI()

    def mt_stop(self):
        self.new_record(logging.LogRecord("LogGui info", 20, "LogGui", -1, "Main thread stopped!", [], None))
        self.setWindowTitle('LogGui - %s - script stopped' % self.name)

    def new_record(self, record):
        row = []
        row.append(QStandardItem(str(datetime.now())))
        self.log_sources.source_list.get_checkbox_state(record.name)
        self.log_sources.level_list.get_checkbox_state("%s (%s)" % (record.levelname, record.levelno))
        name_cell = QStandardItem(record.name)
        name_cell.setData(record, 0x0101)
        if str(record.levelno) in ICON_LEVELS:
            name_cell.setIcon(self.style().standardIcon(ICON_LEVELS[str(record.levelno)]))
        else:
            name_cell.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        row.append(name_cell)
        row.append(QStandardItem("%s (%s)" % (record.levelname, record.levelno)))
        row.append(QStandardItem(record.pathname))
        row.append(QStandardItem(str(record.lineno)))
        row.append(QStandardItem(record.getMessage()))
        if str(record.levelno) in LEVELS_COLOR:
            for i in range(len(row)):
                row[i].setBackground(LEVELS_COLOR[str(record.levelno)][1])
                row[i].setForeground(LEVELS_COLOR[str(record.levelno)][0])
        self.log_view.model.insertRow(0, row)
        self.app.alert(self)

    def show_detailed(self, model_index):
        model_index = model_index.siblingAtColumn(1)
        widgets.LogRecordDialog(model_index.data(0x101)).exec_()

    def initUI(self):
        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('LogGui - loading')
        # Module checklist
        self.main_widget.layout.addWidget(self.log_sources)
        # Log view
        table_columns = "Time, Name, Level, File, Line number, Message".split(", ")
        self.log_view.model = QStandardItemModel()
        self.log_sources.proxy.setSourceModel(self.log_view.model)
        self.log_view.setModel(self.log_sources.proxy)
        self.log_view.model.setColumnCount(len(table_columns))
        self.log_view.model.setHorizontalHeaderLabels(table_columns)
        self.log_view.horizontalHeader().setStretchLastSection(True)
        self.log_view.setEditTriggers(self.log_view.NoEditTriggers)
        self.log_view.setSelectionBehavior(self.log_view.SelectRows)
        self.log_view.doubleClicked.connect(self.show_detailed)
        self.main_widget.layout.addWidget(self.log_view)
        # QMainWindow stuff
        self.main_widget.setLayout(self.main_widget.layout)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setWindowTitle('LogGui - %s - running' % self.name)

    def closeEvent(self, event):
        print("closeEvent")
        event.ignore()
        self.upd_thread.terminate()
        self.main_thread_watch.terminate()
        self.app.exit()
        event.accept()

class GUILoggerHandler(logging.Handler):
    def __init__(self, name_subs=mname):
        self.logqueue = Queue()
        self.name_subs = name_subs
        logging.Handler.__init__(self)
        threading.Thread(target=self._gui_thread).start()
        print("Logging handle added! Check LogGui window!")

    def _gui_thread(self):
        app = QApplication([])
        gl = _GUILog(self.logqueue, app, self.name_subs)
        app.exec_()
        app.exit()
        os._exit(0)

    def emit(self, record):
        self.logqueue.put(record)
