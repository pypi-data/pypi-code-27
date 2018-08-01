from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from db.users_db import list_usernames, find_id, list_contacts
import server
from server import Server
# create main window
class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Users and Connections')
        self.resize(600,600)
        self.setMinimumHeight(400)
        self.setMinimumWidth(450)

        # a widget that allows to have multiple tabs
        tab = QtWidgets.QTabWidget()

        # FIRST TAB
        # a list of current connections
        connectons_list = QtWidgets.QListWidget()
        # TODO: add real current connections later
        for i in range(100):
            connectons_list.addItem(f'Client {i}')
        # create an area that will automatically add a scrollbar
        scrl = QtWidgets.QScrollArea()
        # put connectons_list into the scroll area
        scrl.setWidget(connectons_list)
        # make connectons_list have the same size as the scrollable area
        scrl.setWidgetResizable(True)
        # give content and name to the first tab
        tab.addTab(scrl, 'Current connections')


        # SECOND TAB
        users_tab = QtWidgets.QWidget()
        users_hbox = QtWidgets.QHBoxLayout()

        # create a list view that'll present the model with users
        users_list_view = QtWidgets.QListView()
        # create a model that'll have user names
        sti = QtGui.QStandardItemModel()
        # add each username to the model
        users_list = list_usernames()
        users_list.sort()
        for user in users_list:
            item = QtGui.QStandardItem(user)
            item.setEditable(False)
            sti.appendRow(item)
        users_list_view.setMaximumWidth(200)
        users_list_view.setModel(sti)
        # set single selection mode so that only one user can be selected at a time
        users_list_view.setSelectionMode(1)

        # create user info area
        user_info = QtWidgets.QWidget()
        user_info_vbox = QtWidgets.QVBoxLayout()
        user_info_text = QtWidgets.QLabel('')
        user_info_vbox.addWidget(user_info_text)
        user_info_vbox.setAlignment(QtCore.Qt.AlignTop)
        user_info.setLayout(user_info_vbox)

        def display_user_info(item):
            username = item.data()
            id = find_id(username)
            contacts = ", ".join(list_contacts(id))
            user_info_text.setText(f'<b>Name</b>: {username} <br> <b>id</b>: {id} <br> <b>Contacts</b>: {contacts}')

        users_list_view.clicked.connect(display_user_info)

        users_hbox.addWidget(users_list_view)
        users_hbox.addWidget(user_info)
        users_tab.setLayout(users_hbox)
        tab.addTab(users_tab, 'Users')
        tab.setCurrentIndex(0)

        # MAIN LAYOUT
        mainbox = QtWidgets.QVBoxLayout ()
        mainbox.addWidget(tab)
        self.setLayout(mainbox)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    thread1 = QtCore.QThread()
    Server.moveToThread(thread1)
    thread1.start()
    window.show()
    app.exec_()
