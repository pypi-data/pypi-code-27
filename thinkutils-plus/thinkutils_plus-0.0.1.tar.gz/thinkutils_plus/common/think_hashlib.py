import os
import sys
import hashlib
import requests

def md5_str(szText):
    return str(hashlib.md5(szText).hexdigest())

def MD5(szText):
    m = hashlib.md5()
    m.update(szText)
    return m.digest()

def md5_file(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

# print md5_str("cf43e9194c5e4f7c8cb11469e1d0691c")
# print MD5("cf43e9194c5e4f7c8cb11469e1d0691c")
# print len(MD5("cf43e9194c5e4f7c8cb11469e1d0691c"))