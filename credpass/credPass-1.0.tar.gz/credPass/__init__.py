import os, json

class credPass(object):
    def __init__(self):
        self._path = os.path.expanduser('~/.credentials.json')
    def load(self, host, key):
        with open(self._path, 'r') as f:
            file = json.load(f)
        return file[host].get(key, 'Key not found')
