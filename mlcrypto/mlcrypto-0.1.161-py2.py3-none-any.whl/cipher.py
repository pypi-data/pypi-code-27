import six
import base64
import msgpack
import os


class MsgPackNamedTuple:
    def dumpb(self):
        return msgpack.packb(self._asdict())

    @classmethod
    def loadb(cls, bdata):
        obj_ = {k.decode('utf-8'): v for k, v in msgpack.unpackb(bdata).items()}
        return cls(**obj_)


class Cipher(object):
    @classmethod
    def ensure_bytes(cls, data):
        if six.PY3 and isinstance(data, six.string_types):
            data = data.encode('utf-8')

        return data

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def encrypt_string(self, data):
        bdata = self.ensure_bytes(data)
        encrypted = base64.b64encode(self.encrypt(bdata))
        return encrypted.decode('utf-8')

    def decrypt_string(self, data):
        return self._decrypt_from_string(data).decode('utf-8')

    def encrypt_file_to_str(self, path):
        with open(path, 'rb')as f:
            content = f.read()
            encrypted = base64.b64encode(self.encrypt(content))
            return encrypted.decode('utf-8')

    def _decrypt_from_string(self, data):
        bdata = self.ensure_bytes(data)
        bdata = base64.b64decode(bdata)

        return self.decrypt(bdata)

    def decrypt_string_to_file(self, data, path):
        bdata = self._decrypt_from_string(data)
        with open(path, 'wb')as f:
            f.write(bdata)

        return


def missing_requirement_cipher(requirement):
    class NotImplementedCipher:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError(requirement)

    return NotImplementedCipher
