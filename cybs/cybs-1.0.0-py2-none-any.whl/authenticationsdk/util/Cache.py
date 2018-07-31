import os
from authenticationsdk.util.GlobalLabelParameters import *
from OpenSSL import crypto
import ssl
import base64


class FileCache:

    def __init__(self):
        self.filecache = {}

    def grab_file(self, mconfig, filepath, filename):
        file_mod_time = os.stat(filepath + filename + GlobalLabelParameters.P12_PREFIX).st_mtime
        if not self.filecache.has_key(filename):
            p12 = crypto.load_pkcs12(file(
                filepath + filename + GlobalLabelParameters.P12_PREFIX,
                'rb').read(), mconfig.key_password)
            cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
            der_cert_string = base64.b64encode(ssl.PEM_cert_to_DER_cert(cert_str))
            private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
            self.filecache.setdefault(str(filename), []).append(der_cert_string)
            self.filecache.setdefault(str(filename), []).append(private_key)
            self.filecache.setdefault(str(filename), []).append(file_mod_time)

        if file_mod_time != self.filecache[filename][2]:
            p12 = crypto.load_pkcs12(file(
                filepath + filename + GlobalLabelParameters.P12_PREFIX,
                'rb').read(), mconfig.key_password)
            cert_str = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
            der_cert_string = base64.b64encode(ssl.PEM_cert_to_DER_cert(cert_str))
            private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
            self.filecache.setdefault(str(filename), []).append(der_cert_string)
            self.filecache.setdefault(str(filename), []).append(private_key)
            self.filecache.setdefault(str(filename), []).append(file_mod_time)

        return self.filecache[filename]
