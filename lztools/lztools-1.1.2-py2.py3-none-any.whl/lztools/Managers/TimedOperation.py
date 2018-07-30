import os

import time

class TempPath(object):
    time = None

    def __enter__(self):
        self.time = time.time()
        return self.time

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_path)
