import argparse
import os
import socket
import threading
from PyQt5 import QtCore

from ygram.jim.utils import Utils
from ygram.jim.config import *

def create_parser():
    """
    :return: command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--addr', default='localhost', action='store')
    parser.add_argument('-p', '--port', default=7778, action='store', type=int)
    args = parser.parse_args()
    return args


class ImageServer(QtCore.QObject, Utils):
    """Inherits from QtCore.QObject so that it can be moved to QThread."""
    def __init__(self, addr, port, parent=None):
        super().__init__(parent)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((addr,port))

    def listen(self):
        self.server.listen(15)
        while True:
            print('waiting for a new connection')
            client_connection, addr = self.server.accept()
            print(f'connected to {addr}')
            # starts every new connection in a new thread
            new_connection = threading.Thread(target = self.listen_to_client, args = (client_connection, addr))
            new_connection.start()

    def listen_to_client(self, client_connection, addr):
        print('DEBUG inside listen_to_client addr: ', addr)
        message = self.get_message(client_connection)
        if message[ACTION] == IMAGE:
            self.send_message(client_connection, {RESPONSE: OK})
            message = self.get_message(client_connection)
            if message:
                f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   f'db\profile_images\{message[RESPONSE]}.png'), 'rb')
                print('DEBUG opened image file ')
                image_data = f.read(1024)
                while (image_data):
                    print('DEBUG inside while loop Sending...')
                    client_connection.send(image_data)
                    image_data = f.read(1024)
                f.close()
                print("DEBUG Done Sending")

if __name__ == '__main__':
    args = create_parser()
    image_server = ImageServer(args.addr, args.port)
    image_server.listen()