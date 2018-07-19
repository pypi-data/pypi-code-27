from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import SHA512
from Cryptodome.PublicKey import RSA
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
    def get_cipher_from_bytes(cls, key_bytes, passphrase=None):
        kwargs = {}
        if passphrase is not None:
            kwargs['passphrase'] = passphrase
        key = RSA.importKey(key_bytes, **kwargs)
        return key, PKCS1_OAEP.new(key, hashAlgo=SHA512)

    def __init__(self, key, passphrase=None):
        self.key, self.cipher = self.get_cipher_from_bytes(self.ensure_bytes(key), passphrase=passphrase)
