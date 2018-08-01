from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
import base64

BLOCK_SIZE = 32
KEY = b'86bd8a144720b6b0650cbde99a0db485'
VECTOR = b'0000000011111111'


class CryptAes:
    """
    Класс для шифрования сообщений по алгоритму AES.
    """
    def encrypt(self, message):
        message = message.encode()
        raw = pad(message, BLOCK_SIZE)
        cipher = AES.new(KEY, AES.MODE_CBC, VECTOR)
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, raw_string_crypt):
        raw_string_crypt = base64.b64decode(raw_string_crypt)
        cipher = AES.new(KEY, AES.MODE_CBC, VECTOR)
        dec = cipher.decrypt(raw_string_crypt)
        return unpad(dec, BLOCK_SIZE).decode('utf-8')
