from .asymmetric import Asymmetric


class SshIdentity(Asymmetric):
    def __init__(self, file_path, passphrase=None):
        with open(file_path, 'rb') as f:
            raw_key = f.read()

        super(SshIdentity, self).__init__(raw_key, passphrase=passphrase)

    def export_public_key_bytes(self):
        return self.key.publickey().exportKey('OpenSSH')

    def export_private_key_bytes(self, passphrase=None):
        return self.key.exportKey('PEM', passphrase=passphrase)
