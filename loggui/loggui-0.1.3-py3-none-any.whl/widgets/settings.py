from PyQt5.QtWidgets import QScrollArea, QCheckBox, QVBoxLayout, QSizePolicy, QWidget, QLabel
from PyQt5.QtCore import QSortFilterProxyModel, Qt
import logging
LOGGER = logging.getLogger("LogSettings widget")

class FilterByName(QSortFilterProxyModel):
    def __init__(self, s_checkboxes, l_checkboxes):
        QSortFilterProxyModel.__init__(self)
        self.checkboxes = {
            "1":s_checkboxes,
            "2":l_checkboxes
        }
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, index):
        solution = []
        for row, checkboxes in self.checkboxes.items():
            m_disabled = []
            for name, checkbox in checkboxes.items():
                if not checkbox.isChecked():
                    m_disabled.append(name)
            if self.sourceModel().item(source_row, int(row)).text() in m_disabled:
                solution.append(False)
            else:
                solution.append(True)
        return not False in solution

class CheckList(QScrollArea):

    def __init__(self):
        QScrollArea.__init__(self)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.mlayout = QVBoxLayout()
        mw = QWidget()
        mw.setLayout(self.mlayout)
        self.mlayout.setAlignment(Qt.AlignTop)
        self.setWidget(mw)
        self.checkboxes = {}
        self.setWidgetResizable(True)
        self.setMinimumWidth(200)

    def onchange(self, *_):
        print("OVERRIDE ME!")

    def get_checkbox_state(self, name):
        if not name in self.checkboxes:
            self.checkboxes[name] = QCheckBox(name)
            self.checkboxes[name].setCheckState(2)
            self.checkboxes[name].stateChanged.connect(self.onchange)
            self.mlayout.addWidget(self.checkboxes[name])

class LogSettings(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.source_list = CheckList()
        self.level_list = CheckList()
        self.get_checkbox_state = self.source_list.get_checkbox_state
        self.proxy = FilterByName(self.source_list.checkboxes, self.level_list.checkboxes)
        self.level_list.onchange = self.proxy.invalidateFilter
        self.source_list.onchange = self.proxy.invalidateFilter
        self.mlayout = QVBoxLayout()
        self.mlayout.setAlignment(Qt.AlignTop)
        self.ui_setup()

    def ui_setup(self):
        self.setLayout(self.mlayout)
        self.mlayout.addWidget(QLabel("Log sources:"))
        self.mlayout.addWidget(self.source_list)
        self.mlayout.addWidget(QLabel("Log levels:"))
        self.mlayout.addWidget(self.level_list)
