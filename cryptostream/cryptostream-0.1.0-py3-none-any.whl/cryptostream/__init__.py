from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter
import os
import array
import socket

class Recipient:
    def __init__(self, name, key, url, private_key = None):
        self.name = name
        self.recipient_key = RSA.importKey(key)
        if private_key is not None:
            private_key_object = RSA.importKey(private_key)
            self.priv_cipher_rsa = PKCS1_OAEP.new(private_key_object)
        self.session_key = get_random_bytes(16)
        self.session_iv = get_random_bytes(16)
        self.cipher_rsa = PKCS1_OAEP.new(self.recipient_key)
        self.enc_session_key = self.cipher_rsa.encrypt(self.session_key)
        self.enc_session_iv = self.cipher_rsa.encrypt(self.session_iv)
        ctr = Counter.new(128, initial_value=long(self.session_iv.encode('hex'), 16))
        self.cipher_aes = AES.new(self.session_key, AES.MODE_CTR, counter=ctr)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip, port = url.split(":")
        self.socket.connect((ip, int(port)))
        self.write(self.enc_session_key)
        self.write(self.enc_session_iv)

    def __del__(self):
        self.socket.close()


    def encrypt(self, data):
        ciphertext = self.cipher_aes.encrypt(data)
        self.write(ciphertext)
        return ciphertext

    def decrypt(self, bdata):
        session_key = self.priv_cipher_rsa.decrypt(bdata[:256])
        session_iv = self.priv_cipher_rsa.decrypt(bdata[256:512])
        ctr = Counter.new(128, initial_value=long(session_iv.encode('hex'), 16))
        cipher_aes = AES.new(session_key, AES.MODE_CTR, counter=ctr)
        return cipher_aes.decrypt(bdata[512:])

    def write(self, bdata):
        self.socket.send(bdata)

class CryptoStream:
    def __init__(self):
        self.recipients = list()
        self.prefix = b""

    def add_recipient(self, name, key, url, private_key = None):
        r = Recipient(name, key, url, private_key)
        self.recipients.append(r)
        r.encrypt(self.prefix)
        self.prefix += r.enc_session_key + r.enc_session_iv

    def encrypt(self, data):
        print(len(data))
        for r in self.recipients:
            data = r.encrypt(data)

    def decrypt(self, data, count=None):
        for r in reversed(self.recipients[:count]):
            data = r.decrypt(data)
        return data

    def generate(self, name):
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open(name + ".priv", "wb") as file_out:
            file_out.write(private_key)

        public_key = key.publickey().export_key()
        with  open(name + ".pub", "wb") as file_out:
            file_out.write(public_key)

