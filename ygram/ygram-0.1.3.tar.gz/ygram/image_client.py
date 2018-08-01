import os
import socket
import sys
import threading
from PyQt5 import QtCore

from ygram.jim.utils import Utils
from ygram.jim.config import *


class ImageClient(threading.Thread, Utils):

    def __init__(self, host, port, account_name, contact_name, parent=None):
        super().__init__(parent)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.account_name = account_name
        self.contact_name = contact_name

    def run(self):
        self.send_message(self.client, {ACTION: IMAGE})
        message = self.get_message(self.client)
        if message[RESPONSE] == OK:
            self.send_message(self.client, {RESPONSE: self.contact_name})
            f = open(f'local_client_data\{self.account_name}\{self.contact_name}.png', 'wb')
            image_data = self.client.recv(1024)
            while image_data:
                print("DEBUG Receiving...")
                f.write(image_data)
                if len(image_data) == 1024:
                    image_data = self.client.recv(1024)
                else:
                    break
            f.close()
            mask = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                f'jim\mask.png')
            source_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'local_client_data\{self.account_name}\{self.contact_name}.png')
            output_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                             f'local_client_data\{self.account_name}\{self.contact_name}_circle.png')
            self.make_circular(mask, source_image_path, output_image_path)
            print("DEBUG Done Receiving")
            self.client.close()
            # sys.exit()


if __name__ == '__main__':
    pass
