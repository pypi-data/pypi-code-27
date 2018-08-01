import os
import csv
import time
import socket
import argparse
import threading
from PyQt5 import QtCore


from ygram.errors import *
from ygram.image_client import ImageClient
from ygram.jim.config import *
from ygram.jim.utils import Utils
from ygram.jim.message import PresenceMessage, DeleteContactMessage, TextMessage, AddContactMessage, ListContactsMessage


def create_parser():
    """
    :return: command line arguments: ip address of the server, port of the server, account name
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', default='localhost', action='store')
    parser.add_argument('-p', '--port', default=7777, action='store', type=int)
    parser.add_argument('-an', '--account_name', default='Guest', action='store')

    args = parser.parse_args()

    # checks if account_name is valid
    if len(args.account_name) > 25:
        raise UserNameTooLong(args.account_name)

    for char in args.account_name:
        if char in '!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~ ':
            raise InvalidUserName(args.account_name)
    return args

class Receiver(threading.Thread, Utils):
    """
    A component of client responsible for receiving messages from the server and processing them.
    """
    def __init__(self, sock, contacts_list_signal, add_contact_error_signal, receive_message_signal):
        super().__init__()
        self.sock = sock
        self.contacts_list_signal = contacts_list_signal
        self.add_contact_error_signal = add_contact_error_signal
        self.receive_message_signal = receive_message_signal
    def run(self):
        while True:
            message = self.sock.recv(1024)
            if message:
                # print('DEBUG GOT A MESSAGE!')
                message = self.bytes_to_dict(message)
                if message[ACTION] == LIST_CONTACTS:
                    # print(message[CONTACTS])
                    self.contacts_list_signal.emit(message[CONTACTS])
                    #print('DEBUG emitted contacts_list_signal', message[CONTACTS])
                # is used to open a dialog warning window in case of an error when adding a user
                elif message[ACTION] == ADD:
                    if message[RESPONSE] == 100:
                        print(message[ERROR])
                        self.add_contact_error_signal.emit(message[ERROR])
                        # print('DEBUG emitted add_contact_error_signal')
                    if message[RESPONSE] == OK:
                        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\conversations\{message[ACCOUNT_NAME]}\{message[CONTACT]}.csv'), 'a')
                        f.close()
                        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                              f'local_client_data\conversations\{message[CONTACT]}\{message[ACCOUNT_NAME]}.csv'), 'a')
                        f.close()
                # is used to open a dialog warning window in case of an error when deleting a user
                elif message[ACTION] == DEL:
                    if message[RESPONSE] == 100:
                        print(message[ERROR])
                elif message[ACTION] == MSG:
                    print(f'{message[FROM]} says, "{message[MESSAGE]}"')
                    self.receive_message_signal.emit(message)
                elif message[ACTION] == CONTACT_IMAGE:

                    image_thread = ImageClient('localhost', 7778, message[ACCOUNT_NAME], message[CONTACT_NAME])
                    image_thread.start()
            else:
                continue


class Sender(threading.Thread, Utils):
    """
    A component of client responsible for sending messages to the server
    """
    def __init__(self, sock, account_name):
        super().__init__()
        self.sock = sock
        self.account_name = account_name
    def run(self):
        """
        Is used in the console version of the messenger.
        :return:
        """
        while True:
            text = input(">")
            if (len(text.split()) > 1) and text.startswith('to'):
                _, addressee, *other = text.split()
                text = ' '.join(text.split()[2:])
                message = TextMessage(addressee, text, self.account_name).message
                # print('DEBUG just created text message')
                self.send_message(self.sock, message)
                # print('DEBUG just sent text message')
            elif (len(text.split()) > 1) and text.startswith('add'):
                _, contact, *other = text.split()
                message = AddContactMessage(contact, self.account_name).message
                # print('DEBUG just created text message')
                self.send_message(self.sock, message)
                # print('DEBUG just sent text message')
            elif (len(text.split()) > 1) and text.startswith('del'):
                _, contact, *other = text.split()
                message = DeleteContactMessage(contact, self.account_name).message
                # print('DEBUG just created text message')
                self.send_message(self.sock, message)
                # print('DEBUG just sent text message')
            elif text == 'contacts':
                message = ListContactsMessage(self.account_name).message
                # print('DEBUG just created text message')
                self.send_message(self.sock, message)
                # print("DEBUG just sent contacts ListContactsMessage")
            else:
                print("""
                To send someone a message, type "to Name message". For example "-to Arnold Hello Arnie, how are you today?"\n To add a contact type "add Name"\nTo see your contacts type, "contacts"
                """)

class Client(QtCore.QObject, Utils):
    """
    Inherits from QtCore.QObject so that it can be moved to QThread. Inherits methods from Utils (send_message, receive_message).
    """
    contacts_list_signal = QtCore.pyqtSignal(list)
    add_contact_error_signal = QtCore.pyqtSignal(str)
    delete_contact_error_signal = QtCore.pyqtSignal(str)
    receive_message_signal = QtCore.pyqtSignal(dict)

    def __init__(self, host, port, window, account_name=None, parent=None):
        super().__init__(parent)
        self.account_name = account_name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host,port))
        # first send a presence message
        self.send_message(self.client, PresenceMessage(self.account_name).message)
        response = self.get_message(self.client)
        response = Client.parse_response(response)
        # the main window is used here as an attribute so that we can connect signals to its methods
        self.window = window
        # connect signals to window methods
        # self.window.update_contact_list(response[CONTACTS])
        self.contacts_list_signal.connect(self.window.update_contact_list)
        self.add_contact_error_signal.connect(self.window.add_contact_error)
        self.receive_message_signal.connect(self.window.gui_receive_message)
        self.receiving_thread = Receiver(self.client, self.contacts_list_signal, self.add_contact_error_signal, self.receive_message_signal)
        self.sending_thread = Sender(self.client, self.account_name)

        if response['response'] == OK:
            pass
        else:
            sys.exit("The response should be OK, got {} instead.".format(response['response']))

    def start_threads(self):
        self.receiving_thread.start()
        self.sending_thread.start()

    @staticmethod
    def parse_response(response):
        """
        Makes sure we get a valid response. Otherwise raises an error.
        :param response: dictionary response from server
        :return: dictionary response from server
        """
        if not isinstance(response, dict):
            raise TypeError('Response should be a dictionary, not {}'.format(type(response)))

        if RESPONSE not in 'response':
            raise MandatoryKeyError(RESPONSE)

        code = response[RESPONSE]

        if len(str(code)) != 3:
            raise ResponseCodeLenError(code)
        if code not in RESPONSE_CODES:
            raise ResponseCodeError(code)
        return response

if __name__ == '__main__':
    args = create_parser()
    client = Client(args.addr,args.port, args.account_name)
