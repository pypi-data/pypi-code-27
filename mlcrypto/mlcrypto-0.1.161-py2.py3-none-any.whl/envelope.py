from collections import namedtuple
from .cipher import MsgPackNamedTuple, Cipher
from .symmertric import Symmetric


class EnvelopeData(namedtuple('EnvelopeData', ['data', 'key']), MsgPackNamedTuple):
    pass


class Envelope(Cipher):
    def __init__(self, key_cipher):
        self.key_cipher = key_cipher

    def encrypt_key(self, key):
        return self.key_cipher.encrypt(key)

    def decrypt_key(self, key):
        return self.key_cipher.decrypt(key)

    def encrypt(self, data):
        content_cipher = Symmetric(Symmetric.get_key())
        data = content_cipher.encrypt(data)
        key = self.encrypt_key(content_cipher.key)
        return EnvelopeData(data=data, key=key).dumpb()

    def decrypt(self, data):
        data = EnvelopeData.loadb(data)
        plain_key = self.decrypt_key(data.key)
        content_cipher = Symmetric(plain_key)
        return content_cipher.decrypt(data.data)
