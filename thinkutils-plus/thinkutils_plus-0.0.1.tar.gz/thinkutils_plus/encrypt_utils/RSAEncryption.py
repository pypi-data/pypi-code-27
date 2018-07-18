#!/usr/bin/python
#coding=utf-8

from __future__ import unicode_literals
import base64
import os

import six
from Crypto import Random
from Crypto.PublicKey import *
from abc import *


class PublicKeyFileExists(Exception): pass

class RSAEncryption(object):
    PRIVATE_KEY_FILE_PATH = None
    PUBLIC_KEY_FILE_PATH = None

    def __init__(self, szPublicKeyPath, szPrivateKeyPath):
        self.__private_key = None
        self.__public_key = None
        RSAEncryption.PUBLIC_KEY_FILE_PATH = szPublicKeyPath
        RSAEncryption.PRIVATE_KEY_FILE_PATH = szPrivateKeyPath

    def encrypt(self, message):
        public_key = self._get_public_key()
        public_key_object = RSA.importKey(public_key)
        random_phrase = 'M'
        encrypted_message = public_key_object.encrypt(self._to_format_for_encrypt(message), random_phrase)[0]
        # use base64 for save encrypted_message in database without problems with encoding
        return base64.b64encode(encrypted_message)

    def decrypt(self, encoded_encrypted_message):
        encrypted_message = base64.b64decode(encoded_encrypted_message)
        private_key = self._get_private_key()
        private_key_object = RSA.importKey(private_key)
        decrypted_message = private_key_object.decrypt(encrypted_message)
        return six.text_type(decrypted_message, encoding='utf8')

    def generate_keys(self):
        """Be careful rewrite your keys"""
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        private, public = key.exportKey(), key.publickey().exportKey()

        if os.path.isfile(self.PUBLIC_KEY_FILE_PATH):
            raise PublicKeyFileExists("PublicKeyFileExists")
        #self.create_directories()

        with open(self.PRIVATE_KEY_FILE_PATH, 'w') as private_file:
            private_file.write(private)
        with open(self.PUBLIC_KEY_FILE_PATH, 'w') as public_file:
            public_file.write(public)
        return private, public

    def create_directories(self, for_private_key=True):
        public_key_path = self.PUBLIC_KEY_FILE_PATH.rsplit('/', 1)
        if not os.path.exists(public_key_path):
            os.makedirs(public_key_path)
        if for_private_key:
            private_key_path = self.PRIVATE_KEY_FILE_PATH.rsplit('/', 1)
            if not os.path.exists(private_key_path):
                os.makedirs(private_key_path)

    def _get_public_key(self):
        """run generate_keys() before get keys """
        if self.__public_key is None:
            with open(self.PUBLIC_KEY_FILE_PATH, 'r') as _file:
                self.__public_key = _file.read()
                return self.__public_key
        else:
            return self.__public_key

    def _get_private_key(self):
        """run generate_keys() before get keys """
        if self.__private_key is None:
            with open(self.PRIVATE_KEY_FILE_PATH, 'r') as _file:
                self.__private_key = _file.read()
                return self.__private_key
        else:
            return self.__private_key

    def _to_format_for_encrypt(self,value):
        if isinstance(value, int):
            return six.binary_type(value)
        for str_type in six.string_types:
            if isinstance(value, str_type):
                return value.encode('utf8')
        if isinstance(value, six.binary_type):
            return value

# def main():
#     encrypt = RSAEncryption("../../tcpserver.pub", "../../tcpserver.pem")
#     #encrypt.generate_keys()
#     message = "Hello World"
#     encrypted_msg = encrypt.encrypt(message)
#     print encrypted_msg
#     print encrypt.decrypt(encrypted_msg)
#
# if __name__ == '__main__':
#     main()
