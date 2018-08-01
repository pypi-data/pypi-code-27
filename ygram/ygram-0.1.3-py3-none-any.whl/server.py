import socket
import threading
import argparse
import csv
import sys
import os
from multiprocessing import Process
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from ygram.jim.utils import Utils
from ygram.db.users_db import *
from ygram.jim.config import *
from ygram.jim.message import ListContactsResponseMessage


def create_parser():
    """
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', default='localhost', action='store')
    parser.add_argument('-p', '--port', default=7777, action='store', type=int)
    args = parser.parse_args()
    return args


class Server(QtCore.QObject, Utils):
    """
    Inherits from QtCore.QObject so that it can be moved to QThread. Inherits methods from Utils.
    """

    def __init__(self, addr, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((addr, port))
        # format: {account_name: client socket}
        self.current_connections = {}

    def listen(self):
        self.server.listen(15)
        while True:
            print('waiting for a new connection')
            client_connection, addr = self.server.accept()
            print(f'connected to {addr}')
            # starts every new connection in a new thread
            new_connection = threading.Thread(target=self.listen_to_client, args=(client_connection, addr))
            new_connection.start()

    def listen_to_client(self, client_connection, addr):
        print('DEBUG inside listen_to_client addr: ', addr)
        presence = self.get_message(client_connection)
        response = self.presence_response(presence)
        # print("DEBUG, response is", response)
        # add this connection to the list of current connections
        if presence[USER][ACCOUNT_NAME] in self.current_connections:
            self.current_connections[presence[USER][ACCOUNT_NAME]] = client_connection
        else:
            self.current_connections[addr] = client_connection
        print("DEBUG: current connections:", self.current_connections)
        self.send_message(client_connection, response)

        while True:
            try:
                message = self.get_message(client_connection)
                # print("DEBUG:message:", message) # DEBUG
                # print("DEBUG:message[ACTION]:", message[ACTION])
                actions = {CHECK: self._check_login, ADD_USER: self._add_user, ADD_CONTACT: self._add_contact,
                           DEL_CONTACT: self._del_contact, LIST_CONTACTS: self._list_contacts, MSG: self._send_message}
                # choose the right function from actions
                actions[message[ACTION]](message)

            except Exception as e:
                # client_connection.close()
                # print('DEBUG: Except:', e)
                break

    def _check_login(self, message):
        if check_login_password(message[ACCOUNT_NAME], message[PASSWORD]):
            self.send_message(self.current_connections[tuple(message[ADDR])],
                              {ACTION: CHECK, RESPONSE: OK, CONTACTS: list_contacts(message[ACCOUNT_NAME])})
            self.current_connections[message[ACCOUNT_NAME]] = self.current_connections[tuple(message[ADDR])]
            del self.current_connections[tuple(message[ADDR])]
            print('DEBUG self.current_connections', self.current_connections)
        else:
            self.send_message(self.current_connections[tuple(message[ADDR])], {ACTION: CHECK, RESPONSE: 100})

    def _add_user(self, message):
        print('DEBUG message', message)
        print('DEBUG username_is_used:', username_is_used)
        if not username_is_used(message[ACCOUNT_NAME]):
            print('DEBUG about to add new user')
            print('DEBUG message[IMAGE]:', message[IMAGE])
            os.mkdir(
                os.path.join(os.path.dirname(os.path.realpath(__file__)), f'db\conversations\{message[ACCOUNT_NAME]}'))
            add_user(message[ACCOUNT_NAME], message[PASSWORD])
            self.send_message(self.current_connections[tuple(message[ADDR])], {ACTION: ADD_USER, RESPONSE: OK})
            self.current_connections[message[ACCOUNT_NAME]] = self.current_connections[tuple(message[ADDR])]
            # the next line is needed to get rid of duplicate connections in the connect list, but enabling it will cause the program to crash if a second user is signed up from the same connection due to KeyError
            # del self.current_connections[tuple(message[ADDR])]
            # checks if the user has submitted a custom profile image
            # if so, receives it
            if message[IMAGE] == 'True':
                print('DEBUG about to receive image')
                f = open(f'db\profile_images\{message[ACCOUNT_NAME]}.png', 'wb')
                print("DEBUg open a file")
                image_data = self.current_connections[tuple(message[ADDR])].recv(1024)
                while (image_data):
                    print("DEBUG receiving image...")
                    f.write(image_data)
                    if len(image_data) == 1024:
                        image_data = self.current_connections[tuple(message[ADDR])].recv(1024)
                    else:
                        f.close()
                        print('Done')
                        break

                mask = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    f'jim\mask.png')
                source_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 f'db\profile_images\{message[ACCOUNT_NAME]}.png')
                output_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                 f'db\profile_images\{message[ACCOUNT_NAME]}_circle.png')
                self.make_circular(mask, source_image_path, output_image_path)
            print('DEBUG added new user')
            print('DEBUG self.current_connections', self.current_connections)
        else:
            print('DEBUG such user name is already used')
            print('DEBUG addr to reply', message[ADDR])
            self.send_message(self.current_connections[tuple(message[ADDR])], {ACTION: ADD_USER, RESPONSE: 600})
            print('DEBUG sent a message, username already used')

    def _add_contact(self, message):
        """
        add contact to a client in the database
        :param message: message from a client
        :return: None
        """
        owner = find_id(message[ACCOUNT_NAME])
        contact = find_id(message[CONTACT])

        if contact_user_is_present(contact):
            if not contact_is_present(owner, contact):
                add_contact(owner, contact)
                # self.send_message(sock, {RESPONSE: 200})
                # create csv files for storing conversation history
                f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      f'db\conversations\{message[ACCOUNT_NAME]}\{message[CONTACT]}.csv'), 'a')
                f.close()
                f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                      f'db\conversations\{message[CONTACT]}\{message[ACCOUNT_NAME]}.csv'), 'a')
                f.close()
                # checks if the contact user has a custom profile image and if so, send it
                image = Path(f"db\profile_images\{message[CONTACT]}.png")
                self.send_message(self.current_connections[message[ACCOUNT_NAME]],
                                  {ACTION: ADD, RESPONSE: 200, ACCOUNT_NAME: message[ACCOUNT_NAME], CONTACT: message[CONTACT]})

                if image.is_file():
                    self.send_message(self.current_connections[message[ACCOUNT_NAME]],
                                      {ACTION: CONTACT_IMAGE, ACCOUNT_NAME: message[ACCOUNT_NAME],
                                       CONTACT_NAME: message[CONTACT]})
            else:
                self.send_message(self.current_connections[message[ACCOUNT_NAME]],
                                  {ACTION: ADD, RESPONSE: 100, ERROR: 'This user is already in contacts'})
        else:
            self.send_message(self.current_connections[message[ACCOUNT_NAME]],
                              {ACTION: ADD, RESPONSE: 100, ERROR: 'No user with such name'})

    def _del_contact(self, message):
        """
        delete contact form a client in the database
        :param message: message from a client
        :return: None
        """
        owner = find_id(message[ACCOUNT_NAME])
        contact = find_id(message[CONTACT])
        if contact_is_present(owner, contact):
            delete_contact(owner, contact)
            self.send_message(self.current_connections[message[ACCOUNT_NAME]], {ACTION: DEL, RESPONSE: 200})
        else:
            self.send_message(self.current_connections[message[ACCOUNT_NAME]],
                              {ACTION: DEL, RESPONSE: 100, ERROR: 'This user is not in contacts'})

    def _send_message(self, message):
        """
        send p2p message, keep it on the server
        :param message:
        :return:
        """
        # print("DEBUG: message p2p", message)
        # print("DEBUG: message to", message[TO])
        # print("DEBUG: message from", message[FROM])
        try:
            self.send_message(self.current_connections[message[TO]], message)

        except KeyError:  # the addressee is currently offline
            # TODO later
            pass

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               f'db\conversations\{message[FROM]}\{message[TO]}.csv'), 'a', newline='\n',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([1, message[MESSAGE], message[TIME]])
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               f'db\conversations\{message[TO]}\{message[FROM]}.csv'), 'a', newline='\n',
                  encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([0, message[MESSAGE], message[TIME]])

    def _list_contacts(self, message):
        """
        get a list of contacts of a particular user
        :param message:
        :return:
        """
        # print('DEBUG about to send ListContactsResponseMessage')
        message = ListContactsResponseMessage(message[ACCOUNT_NAME], list_contacts(message[ACCOUNT_NAME])).message
        # print('DEBUG message:', message)
        self.send_message(self.current_connections[message[ACCOUNT_NAME]], message)

    def presence_response(self, presence_message: dict) -> dict:
        """
        Creates a response to a presence message
        :param presence_message: presence message received from client in the dictionary format
        :return: response in the dictionary format
        """
        # print("DEBUG: presence_message:", presence_message)
        if ACTION in presence_message and presence_message[
            ACTION] == PRESENCE and TIME in presence_message and isinstance(presence_message[TIME], float):
            # if no such user in database, add him or her and create a folder in conversations folder where his or her conversations with other users will be held
            return {RESPONSE: 200}  # , CONTACTS: presence_message[CONTACTS]}
        else:
            # Error
            return {RESPONSE: 400, ERROR: 'Invalid request'}


if __name__ == '__main__':
    args = create_parser()
    server = Server(args.addr, args.port)
    server.listen()
