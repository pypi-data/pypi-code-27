import binascii
import csv
import hashlib
import os
import sys
import textwrap
import time
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from PIL import Image, ImageOps

from ygram.client import *
from ygram.db.users_db import find_id, list_contacts, username_is_used, add_user
from ygram.image_client import ImageClient
from ygram.jim.config import *
from ygram.jim.message import AddContactMessage, ListContactsMessage, TextMessage, AddUserMessage, CheckLoginMessage


# create main window
class MainWindow(QtWidgets.QWidget):
    """
    Main GUI window
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('YGram')
        self.setMinimumHeight(400)
        self.setFixedWidth(760)
        self.resize(760, 760)
        # <editor-fold desc="LEFT SIDE">
        self.left_side = QtWidgets.QWidget()
        self.left_side.setMaximumWidth(200)

        def add_contact():
            """
            Is called upon clicking button "add contact". Opens a dialog window with an input field.
            :return: None
            """
            contact, result = QtWidgets.QInputDialog.getText(self, 'Add contact', 'Enter username:')
            if result:
                # print('DEBUG pressed ok, name:', contact)
                # print('DEBUG client.account_name:', client.account_name)
                # print('contact:', contact)
                message = AddContactMessage(contact, client.account_name).message
                client.send_message(client.client, message)
                message = ListContactsMessage(client.account_name).message
                # print('DEBUG message to send:', message)
                client.send_message(client.client, message)
                # print("DEBUG just sent contacts ListContactsMessage")
            else:
                # print('DEBUG pressed cancel')
                pass

        # <editor-fold desc="add button">
        self.add_button = QtWidgets.QPushButton('Add Contact')
        self.add_button.clicked.connect(add_contact)
        self.del_button = QtWidgets.QPushButton('Delete Contact')
        self.del_button.clicked.connect(self.del_contact)
        # </editor-fold>

        # <editor-fold desc="contacts list">
        self.contacts_list_view = QtWidgets.QListWidget()
        self.contacts_list_view.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.contacts_list_view.setSelectionMode(1)
        self.contacts_list_view.clicked.connect(self.load_message_history)
        # </editor-fold>

        # <editor-fold desc="set left side layout">
        self.left_side_box = QtWidgets.QVBoxLayout()
        self.left_side_box.setContentsMargins(5, 5, 0, 5)
        self.left_side_box.addWidget(self.add_button)
        self.left_side_box.addWidget(self.del_button)
        self.left_side_box.addWidget(self.contacts_list_view)
        self.left_side.setLayout(self.left_side_box)
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="RIGHT SIDE">
        self.right_side = QtWidgets.QWidget()

        # <editor-fold desc="message history area">
        self.MessageAreaList = QtWidgets.QListWidget()
        self.MessageAreaList.setFrameStyle(QtWidgets.QFrame.NoFrame)
        # makes scrolling smooth: by pixel, no by item
        self.MessageAreaList.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.MessageAreaList.setStyleSheet('font-size: 11pt;')
        # </editor-fold>

        # the bottom area with the input field and send button
        self.bottom_line = QtWidgets.QWidget()

        # <editor-fold desc="message input field">
        self.input_field = QtWidgets.QTextEdit()
        self.input_field.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.input_field.setPlaceholderText('Write a message...')
        self.input_field.setFixedHeight(100)
        self.input_field.setStyleSheet('font-size: 11pt;')
        # </editor-fold>

        # <editor-fold desc="send button">
        self.send_button = QtWidgets.QPushButton('Send')
        self.send_button.clicked.connect(self.gui_send_message)
        # </editor-fold>

        # <editor-fold desc="set bottom line layout">
        self.bottom_line_box = QtWidgets.QHBoxLayout()
        self.bottom_line_box.setContentsMargins(0, 0, 0, 0)
        self.bottom_line_box.addWidget(self.input_field)
        self.bottom_line_box.addWidget(self.send_button)
        self.bottom_line.setLayout(self.bottom_line_box)
        # </editor-fold>

        # <editor-fold desc="set right side layout">
        self.right_side_box = QtWidgets.QVBoxLayout()
        self.right_side_box.addWidget(self.MessageAreaList, 1)
        self.right_side_box.addWidget(self.bottom_line)
        self.right_side_box.setContentsMargins(5, 5, 5, 5)
        self.right_side.setLayout(self.right_side_box)
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="set mainbox layout">
        self.setContentsMargins(0, 0, 0, 0)
        self.mainbox = QtWidgets.QHBoxLayout()
        self.mainbox.setSpacing(0)
        self.mainbox.addWidget(self.left_side)
        self.mainbox.addWidget(self.right_side)
        self.setLayout(self.mainbox)
        # </editor-fold>

    def update_contact_list(self, contact_list):
        """
        :param contact_list: a list of user names
        :return: None
        """

        for contact in sorted(contact_list):
            item = ContactItem(contact)
            custom_line = ContactLine(contact)
            item.setSizeHint(custom_line.sizeHint())
            self.contacts_list_view.addItem(item)
            self.contacts_list_view.setItemWidget(item, custom_line)

    def del_contact(self):
        del_dialog = QtWidgets.QMessageBox(self)
        del_dialog.setWindowTitle('Deleting user from contacts')
        if self.contacts_list_view.selectedIndexes():
            # get the first (and only) selected username from the contacts list
            username = self.contacts_list_view.selectedIndexes()[0].data()
            del_dialog.setText(f'Delete user {username} from contacts?')
            del_dialog.addButton(QtWidgets.QMessageBox.Yes)
            del_dialog.addButton(QtWidgets.QMessageBox.No)
            result = del_dialog.exec_()
            if result == QtWidgets.QMessageBox.Yes:
                message = DeleteContactMessage(username, client.account_name).message
                client.send_message(client.client, message)
                message = ListContactsMessage(client.account_name).message
                # print('DEBUG message to send:', message)
                client.send_message(client.client, message)
                # print("DEBUG just sent contacts ListContactsMessage")
            else:
                # print('DEBUG No pressed, doing nothing')
                pass
        else:
            # if no user selected
            del_dialog.setText('First select a user that you want to delete')
            del_dialog.exec_()

    def add_contact_error(self, text):
        """
        Opens a dialog window upon getting the signal (due to an error: no such user or already in contacts)
        :param text: error message
        :return: None
        """
        add_dialog = QtWidgets.QMessageBox(self)
        add_dialog.setWindowTitle('Adding contact error')
        add_dialog.setText(text)
        add_dialog.exec_()

    def gui_send_message(self):
        if self.contacts_list_view.selectedIndexes():
            # get the first (and the only) selected username from the contacts list
            # "to" is the user name that the message is sent to

            to = self.contacts_list_view.currentItem().username
            # get the text from the input field
            # text = f'{self.input_field.toPlainText()}'
            print('DEBUG text to send:', self.input_field.toPlainText())
            text = self.input_field.toPlainText().split('\n')
            text = (textwrap.fill(el, 45) for el in text)
            text = '\n'.join(text)
            # print(f"DEBUG to {to}:", text)
            # add the message to the message history
            now = time.time()
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   f'local_client_data\conversations\{client.account_name}\{to}.csv'), 'a',
                      newline='\n',
                      encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([1, self.input_field.toPlainText(), now])
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   f'local_client_data\conversations\{to}\{client.account_name}.csv'), 'a',
                      newline='\n',
                      encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([0, self.input_field.toPlainText(), now])
            # an item to be added to the message history
            item = QtWidgets.QListWidgetItem()
            custom_message = MessageLine(text, now, client.account_name)
            item.setSizeHint(custom_message.sizeHint())
            self.MessageAreaList.addItem(item)
            self.MessageAreaList.setItemWidget(item, custom_message)
            self.MessageAreaList.scrollToBottom()
            message = TextMessage(to, self.input_field.toPlainText(), client.account_name).message
            client.send_message(client.client, message)
            self.input_field.clear()
        else:
            # if no user selected
            dialog = QtWidgets.QMessageBox(self)
            dialog.setWindowTitle('Warning')
            dialog.setText('First select a user.')
            dialog.exec_()

    def gui_receive_message(self, message):
        # print("DEBUG received message:", message)
        # print('DEBUG selected', [item.data() for item in contacts_list_view.selectedIndexes()])
        if self.contacts_list_view.selectedIndexes():
            from_user = self.contacts_list_view.currentItem().username
            if from_user == message[FROM]:
                text = textwrap.fill(message[MESSAGE], 45)
                item = QtWidgets.QListWidgetItem()
                custom_message = MessageLine(text, message[TIME], message[FROM])
                item.setSizeHint(custom_message.sizeHint())
                self.MessageAreaList.addItem(item)
                self.MessageAreaList.setItemWidget(item, custom_message)
                self.MessageAreaList.scrollToBottom()

    def load_message_history(self):
        """
        Loads message history of the client with a particular user and displays it in the message area
        :return:
        """
        # print("DEBUG contact name row:", contact_name.row())
        # print("DEBUG current item:", self.contacts_list_view.currentItem())
        # print("DEBUG current item username:", self.contacts_list_view.currentItem().username)
        self.MessageAreaList.clear()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            f'local_client_data\conversations\{client.account_name}\{self.contacts_list_view.currentItem().username}.csv')
        with open(path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            last_date = '01/01/01'
            this_date = None

            for row in reader:
                this_date = time.strftime('%D', time.localtime(float(row[2])))
                if this_date != last_date:
                    item = QtWidgets.QListWidgetItem(f'\n{this_date}\n')
                    item.setTextAlignment(QtCore.Qt.AlignHCenter)
                    self.MessageAreaList.addItem(item)
                last_date = this_date

                if int(row[0]):
                    text = textwrap.fill(row[1], 45)
                    item = QtWidgets.QListWidgetItem()
                    custom_message = MessageLine(text, row[2], client.account_name)
                    item.setSizeHint(custom_message.sizeHint())
                    self.MessageAreaList.addItem(item)
                    self.MessageAreaList.setItemWidget(item, custom_message)
                else:
                    text = textwrap.fill(row[1], 45)
                    item = QtWidgets.QListWidgetItem()
                    custom_message = MessageLine(text, row[2], self.contacts_list_view.currentItem().username)
                    item.setSizeHint(custom_message.sizeHint())
                    self.MessageAreaList.addItem(item)
                    self.MessageAreaList.setItemWidget(item, custom_message)

        self.MessageAreaList.scrollToBottom()


class Login(QtWidgets.QWidget):
    """
    Login window that is the first one to open when the program is launched
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Log in')

        self.box = QtWidgets.QGridLayout()

        # <editor-fold desc="new user button">
        self.new_user_button = QtWidgets.QPushButton('New user?')
        self.new_user_button.clicked.connect(self.new_user)
        # </editor-fold>

        # <editor-fold desc="username and password labels and input fields">
        self.username_label = QtWidgets.QLabel('Login:')
        self.password_label = QtWidgets.QLabel('Password:')
        self.username_input_field = QtWidgets.QLineEdit()
        self.password_input_field = QtWidgets.QLineEdit()
        self.password_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        # </editor-fold>

        # <editor-fold desc="button box">
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(app.quit)
        # </editor-fold>

        # <editor-fold desc="set layout">
        self.box.addWidget(self.new_user_button, 0, 1)
        self.box.addWidget(self.username_label, 1, 0)
        self.box.addWidget(self.username_input_field, 1, 1)
        self.box.addWidget(self.password_label, 2, 0)
        self.box.addWidget(self.password_input_field, 2, 1)
        self.box.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.setLayout(self.box)
        # </editor-fold>

    def accept(self):
        username = self.username_input_field.text()
        password = self.password_input_field.text()
        password = bytes(password, encoding='utf-8')
        try:
            with open(f'salt\{username}_salt.txt', 'rb') as f:
                salt = f.read()
            h = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
            hash_sum = str(binascii.hexlify(h))
            message = CheckLoginMessage(username, hash_sum, client.client.getsockname()).message
            client.send_message(client.client, message)
            response = client.get_message(client.client)
            # print("DEBUG, message:", message)
            if message:
                if response[ACTION] == CHECK and response[RESPONSE] == OK:
                    client.account_name = username
                    print('I am', client.account_name)
                    client.start_threads()
                    self.close()
                    window.setWindowTitle(f'BlahBlahGram - {username}')
                    window.show()
                    window.update_contact_list(response[CONTACTS])
                else:
                    add_user_fail_dialog = QtWidgets.QMessageBox(self)
                    add_user_fail_dialog.setWindowTitle('Error')
                    add_user_fail_dialog.setText('Invalid username or password')
                    add_user_fail_dialog.exec_()
        except FileNotFoundError:
            self.error_window('Invalid username or password')

    def new_user(self):
        self.hide()
        global signup
        if not signup:
            signup = Signup()
            signup.show()
        else:
            signup.show()

    def error_window(self, text):
        """
        Creates a generic dialog window with an error message
        :param text:
        :return:
        """
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText(text)
        error_dialog.exec_()


class Signup(QtWidgets.QWidget):
    """
    A sign up window to create a new account. Has login and password fields.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_profile_image = False
        self.setWindowTitle('Sign up')
        self.setFixedSize(250, 350)
        self.box = QtWidgets.QVBoxLayout()

        # <editor-fold desc="buttons and labels">
        self.grid_widget = QtWidgets.QWidget()
        self.grid_widget.setContentsMargins(5, 5, 5, 0)
        self.grid_box = QtWidgets.QGridLayout()
        self.username_label = QtWidgets.QLabel('Login:')
        self.password_label = QtWidgets.QLabel('Password:')
        self.select_image_label = QtWidgets.QLabel('Profile image:')
        self.username_input_field = QtWidgets.QLineEdit()
        self.password_input_field = QtWidgets.QLineEdit()
        self.password_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.select_image_button = QtWidgets.QPushButton('Select image')
        self.select_image_button.clicked.connect(self.select_image)
        self.remove_image_button = QtWidgets.QPushButton('Remove image')
        self.remove_image_button.clicked.connect(self.remove_image)

        # <editor-fold desc="set grid layout">
        self.grid_box.addWidget(self.username_label, 0, 0)
        self.grid_box.addWidget(self.username_input_field, 0, 1)
        self.grid_box.addWidget(self.password_label, 1, 0)
        self.grid_box.addWidget(self.password_input_field, 1, 1)
        self.grid_box.addWidget(self.select_image_label, 2, 0)
        self.grid_box.addWidget(self.select_image_button, 2, 1)
        self.grid_box.addWidget(self.remove_image_button, 3, 1)
        self.grid_widget.setLayout(self.grid_box)
        # </editor-fold>
        # </editor-fold>

        # <editor-fold desc="image area">
        self.image_widget = QtWidgets.QWidget()
        self.image_widget_box = QtWidgets.QHBoxLayout()
        self.image_widget_box.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label = QtWidgets.QLabel()
        self.image_label.setScaledContents(False)
        path_to_standard_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'db\profile_images\standard.png')
        self.image_label.setPixmap(QtGui.QPixmap(path_to_standard_image))
        self.image_label.show()
        self.image_widget_box.addWidget(self.image_label)
        self.image_widget.setLayout(self.image_widget_box)
        # </editor-fold>
        print('DEBUG self.image_widget width', self.image_widget.width())
        # <editor-fold desc="ok cancel button box">
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # </editor-fold>

        self.box.addWidget(self.grid_widget)
        self.box.addWidget(self.image_widget)
        self.box.addWidget(self.buttonBox)
        self.setLayout(self.box)

    def accept(self):
        not_accepted = False
        username = self.username_input_field.text()
        password = self.password_input_field.text()

        # print("DEBUG, log, pass:", login, password)

        if len(username) == 0 or len(password) == 0:
            self.error_window(f"Please enter both login and password")
            not_accepted = True
        elif len(username) > 25 or len(username) < 2:
            self.error_window(
                f"Username must not have less than 2 or more than 25 characters in it. The length of the given username is {len(self.login)}.")
            not_accepted = True
        elif len(password) > 20 or len(password) < 8:
            self.error_window(
                f"Password must not have less than 8 or more than 20 characters in it. The length of the given password is {len(password)}.")
            not_accepted = True
        for char in username:
            if char in '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ ':
                self.error_window("Username may have only letters, numbers and underscore in it.")
                not_accepted = True
                break

        if not not_accepted:
            # print('DEBUG username and password accepted')
            password = bytes(password, encoding='utf-8')
            salt = os.urandom(128)
            # print('DEBUG salt created')
            # TODO encrypt salt
            with open(f'salt\{username}_salt.txt', 'wb') as f:
                f.write(salt)
            # print('DEBUG file created')
            h = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
            # print('DEBUG has object created')
            hash_sum = str(binascii.hexlify(h))
            message = AddUserMessage(username, hash_sum, client.client.getsockname(), self.custom_profile_image).message
            # print('DEBUG created message', message)
            client.send_message(client.client, message)
            # print('DEBUG sent a message to add user')
            message = client.get_message(client.client)
            # print("DEBUG, message:", message)
            if message:
                if message[ACTION] == ADD_USER and message[RESPONSE] != OK:
                    # print('DEBUG This user name is already used')
                    self.error_window('Such username is already used. Please choose another one.')
                else:
                    os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'local_client_data\{username}'))
                    os.mkdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                          f'local_client_data\conversations\{username}'))
                    # if the user has submitted a custom profile picture, send it ot the server
                    if self.custom_profile_image:
                        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              'temp.png'), 'rb')
                        image = f.read(1024)
                        while (image):
                            print('DEBUG inside while loop Sending...')
                            client.client.send(image)
                            image = f.read(1024)
                        f.close()
                        os.rename(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp.png'),
                                  os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                               f'local_client_data\{username}\{username}.png'))

                        mask = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            f'jim\mask.png')
                        source_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                         f'local_client_data\{username}\{username}.png')
                        output_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                         f'local_client_data\{username}\{username}_circle.png')
                        client.make_circular(mask, source_image_path, output_image_path)
                    add_user_success_dialog = QtWidgets.QMessageBox(self)
                    add_user_success_dialog.setWindowTitle('Welcome')
                    add_user_success_dialog.setText('Now log in with your username and password')
                    add_user_success_dialog.exec_()
                    self.remove_image()
                    self.close()
                    self.username_input_field.clear()
                    self.password_input_field.clear()
                    login.show()

    def reject(self):
        self.close()
        login.show()

    def error_window(self, text):
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setWindowTitle('Error')
        error_dialog.setText(text)
        error_dialog.exec_()

    def select_image(self):
        dir = os.getcwd()
        filters = "Images (*.png *.jpg)"
        selected_filter = "Images (*.png *.jpg)"
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, " File dialog ", dir, filters, selected_filter)
        if file_name:
            print('DEBUG file name:', file_name[0])
            self.display_image(file_name[0])
            self.custom_profile_image = True

    def display_image(self, path_to_image):
        print('DEBUG inside display func')
        print('DEBUG self.username_input_field.text():', self.username_input_field.text())
        image = Image.open(path_to_image)
        thumb = ImageOps.fit(image, (134, 134), Image.ANTIALIAS)
        thumb.save('temp.png')
        self.image_label.setPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                              'temp.png')))

    def remove_image(self):
        path_to_standard_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'db\profile_images\standard.png')
        self.image_label.setPixmap(QtGui.QPixmap(path_to_standard_image))
        self.custom_profile_image = False


class MessageLine(QtWidgets.QWidget):
    def __init__(self, text, now, username, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.left = QtWidgets.QWidget()
        self.left.setFixedWidth(395)
        self.left_box = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(45, 45)
        self.image_label.setScaledContents(True)
        image = Path(f"local_client_data\{client.account_name}\{username}_circle.png")
        if image.is_file():
            self.path_to_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\{client.account_name}\{username}_circle.png')
            self.image_label.setPixmap(QtGui.QPixmap(self.path_to_image))
        else:
            self.path_to_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\standard.png')
            self.image_label.setPixmap(QtGui.QPixmap(self.path_to_image))
        self.text_label = QtWidgets.QLabel(text)
        number_of_new_lines = len(text.split('\n'))
        if number_of_new_lines >= 3:
            self.text_label.setMinimumHeight(number_of_new_lines * 20)
        self.left_box.addWidget(self.image_label)
        self.left_box.insertSpacing(1, 10)
        self.left_box.addWidget(self.text_label)
        self.left_box.setAlignment(self.image_label, QtCore.Qt.AlignTop)
        self.left_box.setAlignment(self.text_label, QtCore.Qt.AlignVCenter)
        self.left.setLayout(self.left_box)

        # <editor-fold desc="right side">
        self.right = QtWidgets.QWidget()
        self.right_box = QtWidgets.QHBoxLayout()
        self.time_label = QtWidgets.QLabel(time.strftime('%H:%M:%S', time.localtime(float(now))))
        self.time_label.setMaximumWidth(55)
        self.right_box.addWidget(self.time_label)
        self.right_box.setAlignment(self.time_label, QtCore.Qt.AlignVCenter)
        self.right.setLayout(self.right_box)
        # </editor-fold>

        # <editor-fold desc="set main layout">
        self.layout.addWidget(self.left)
        self.layout.addWidget(self.right)
        # self.layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        # </editor-fold>


class ContactLine(QtWidgets.QWidget):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username
        self.layout = QtWidgets.QHBoxLayout()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(45, 45)
        self.image_label.setScaledContents(True)
        image = Path(f"local_client_data\{self.username}\{self.username}_circle.png")
        if image.is_file():
            self.path_to_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\{self.username}\{username}_circle.png')
            self.image_label.setPixmap(QtGui.QPixmap(self.path_to_image))
        else:
            self.path_to_image = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\standard.png')
            self.image_label.setPixmap(QtGui.QPixmap(self.path_to_image))
        self.text_label = QtWidgets.QLabel(username)
        self.layout.addWidget(self.image_label)
        self.layout.insertSpacing(1, 10)
        self.layout.addWidget(self.text_label)
        # self.left_box.setAlignment(self.image_label, QtCore.Qt.AlignTop)
        self.layout.setAlignment(self.text_label, QtCore.Qt.AlignVCenter)
        self.setLayout(self.layout)


class ContactItem(QtWidgets.QListWidgetItem):
    def __init__(self, username, parent=None):
        super().__init__(parent)
        self.username = username


if __name__ == '__main__':
    args = create_parser()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    client = Client(args.addr, args.port, window)
    client_thread = QtCore.QThread()
    client.moveToThread(client_thread)
    client_thread.start()
    signup = False
    login = Login()
    login.show()
    sys.exit(app.exec_())
