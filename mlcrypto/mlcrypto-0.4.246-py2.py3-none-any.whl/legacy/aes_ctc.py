from mlcrypto.crypto_lib import CryptoLib
from mlcrypto.symmertric import Symmetric
from CryptoLib.Cipher import AES


class AesCtc(Symmetric):
    @classmethod
    def _pad_str_to_len(cls, s, pad_len=32):
        return s + (pad_len - len(s) % pad_len) * ' '.encode('utf-8')

    def get_cipher(self, iv):
        return AES.new(self.key, AES.MODE_CBC, iv)

    def encrypt(self, data):
        return super(AesCtc, self).encrypt(self._pad_str_to_len(data))

    def decrypt(self, data):
        return super(AesCtc, self).decrypt(data).strip()
