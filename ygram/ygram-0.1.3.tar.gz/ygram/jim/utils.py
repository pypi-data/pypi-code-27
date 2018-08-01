import json
import time
import os
from PIL import Image, ImageOps

class Utils:

    def __init__(self, encoding='utf-8'):
        self.ENCODING = encoding

    # @staticmethod
    def dict_to_bytes(self, message_dict: dict) -> bytes:
        """
        :param message_dict: dictionary
        :return: bytes
        """
        if isinstance(message_dict, dict):
            # dict to json
            jmessage = json.dumps(message_dict)
            # json to bytes
            bmessage = jmessage.encode('utf-8')
            return bmessage
        else:
            raise TypeError(
                'The argument should be of type dict, but an argument of type {} was given'.format(type(message_dict)))

    # @staticmethod
    def bytes_to_dict(self, message_dict: bytes) -> dict:
        """
        :param message_dict: bytes
        :return: dictionary
        """
        if isinstance(message_dict, bytes):
            # bytes to json
            jmessage = message_dict.decode('utf-8')
            # json to dict
            message = json.loads(jmessage)
            if isinstance(message, dict):
                return message
            else:
                raise TypeError(
                    'The message should be of type dict, but a message of type {} was sent'.format(type(message)))
        else:
            raise TypeError(
                'The message should be of type bytes, but a message of type {} was sent'.format(type(message_dict)))


    def send_message(self, sock, message: dict):
        """
        :param sock: socket
        :param message: dictionary message
        :return: None
        """
        # dict to byts
        bprescence = self.dict_to_bytes(message)
        # send
        sock.send(bprescence)

    def get_message(self, sock):
        """
        :param sock: socket
        :return:
        """
        # receive message
        bmessage = sock.recv(1024)
        # bytes to dict
        message = self.bytes_to_dict(bmessage)
        return message

    def make_circular(self, mask_source_path, image_source_path, image_output_path):
        mask = Image.open(mask_source_path).convert('L')
        image = Image.open(image_source_path)
        thumb = ImageOps.fit(image, (134, 134), Image.ANTIALIAS)
        thumb.putalpha(mask)
        thumb.save(image_output_path)