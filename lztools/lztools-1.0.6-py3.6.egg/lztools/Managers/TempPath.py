import os

class TempPath(object):
    original_path = None
    new_path = None

    def __init__(self, path):
        self.original_path = os.getcwd()
        self.new_path = os.path.realpath(path)

    def __enter__(self):
        os.chdir(self.new_path)
        return self.new_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_path)
