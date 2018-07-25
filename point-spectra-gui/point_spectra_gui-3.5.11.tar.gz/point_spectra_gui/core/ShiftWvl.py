import pandas as pd
from PyQt5 import QtWidgets
from point_spectra_gui.util.spectral_data import spectral_data

from point_spectra_gui.ui.ShiftWvl import Ui_Form
from point_spectra_gui.util.Modules import Modules
from libpysat.transform.shift_spect import shift_spect

class ShiftWvl(Ui_Form, Modules):
    """
    Loads the data into the UI.
    The data needs to be a *.csv in order for this application to work
    """

    def setupUi(self, Form):
        super().setupUi(Form)
        Modules.setupUi(self, Form)

    def get_widget(self):
        return self.groupLayout


    def connectWidgets(self):
        self.setComboBox(self.choosedata, self.datakeys)


    def run(self):
        datakey_to_shift = self.choosedata.currentText()
        shifts = [float(i) for i in self.shifts.text().split(',')]
        pass
        self.data[datakey_to_shift].df[('meta','Shift')] = 0
        to_shift = self.data[datakey_to_shift].df
        for s in shifts:
            shifted = shift_spect(to_shift,s)
            self.data[datakey_to_shift].df = pd.concat([self.data[datakey_to_shift].df, shifted])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    Form = QtWidgets.QWidget()
    ui = ShiftWvl()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
