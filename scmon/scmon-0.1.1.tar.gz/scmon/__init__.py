"""Restart apps upon source code change.

Taken from https://jesper.borgstrup.dk/wp-content/uploads/2011/10/SourceChangeMonitor.py

Modified by krisfris.
"""

import os
import sys
import time
import fnmatch
import subprocess


POLL_INTERVAL = 1
FILE_PATTERN = r"[!.]*.py"


class SourceChangeMonitor:
    _process = None

    def __init__(self, rootdir, popen_args):
        self.rootdir = rootdir
        self.popen_args = popen_args
        self.this_script_name = os.path.abspath(sys.argv[0])
        self.files = self.get_files()
        self.start_program()

    def run(self):
        while 1:
                time.sleep(POLL_INTERVAL)
                if self.poll():
                        print("-------------------------------------------------")
                        print("Noticed a change in program source. Restarting...")
                        print("-------------------------------------------------")
                        self.start_program()

    def get_files(self):
        files = []
        for root, dirnames, filenames in os.walk(self.rootdir):
                for filename in fnmatch.filter(filenames, FILE_PATTERN):
                        full_filename = os.path.join(root, filename)
                        files.append(full_filename)

        # Attach the last modified dates
        files = [(x, os.stat(x).st_mtime) for x in files]

        # Don't include this script
        files = filter(lambda x: x[0] != self.this_script_name, files)

        return list(files)

    def poll(self):
        new_files = self.get_files()
        if self.files != new_files:
            self.files = new_files
            return True
        return False

    def start_program(self):
        if self._process is not None and self._process.poll() is None:
                self._process.kill()
                self._process.wait()

        self._process = subprocess.Popen(self.popen_args)


if __name__ == '__main__':
    mon = SourceChangeMonitor('./scmon', [sys.executable, 'm', 'myapp.main'])
    mon.run()
