from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from .cipher import Cipher


class Asymmetric(Cipher):
    KEY = 'PKCS1_OAEP-SHA512'

    @classmethod
    def get_key_pair(cls, size=4096):
        key = RSA.generate(size)
        private = key.exportKey('PEM')
        public = key.publickey().exportKey('PEM')
        return private.decode('utf-8'), public.decode('utf-8')

    @classmethod
    def get_cipher(cls, key_bytes):
        key = RSA.importKey(key_bytes)
        return PKCS1_OAEP.new(key, hashAlgo=SHA512)

    def __init__(self, key):
        self.key = self.ensure_bytes(key)
        self.cipher = self.get_cipher(key)
