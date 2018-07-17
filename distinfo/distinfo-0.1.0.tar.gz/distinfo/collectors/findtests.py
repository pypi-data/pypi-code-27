import subprocess

from .collector import Collector


class FindTests(Collector):

    def _collect(self):
        self.dist.ext.tests = bool(
            subprocess.check_output(("find", ".", "-name", "test*.py")).strip()
        )
