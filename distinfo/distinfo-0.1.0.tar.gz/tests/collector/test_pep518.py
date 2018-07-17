from distinfo import Requirement
from distinfo.collectors import Pep518

from .cases import TestCase

SETUP = """
from setuptools import setup
setup()
"""

PYPROJECT = """
[build-system]
requires = ["zzz"]
"""


class TestPep518(TestCase):

    collector = Pep518

    def test_collect(self, tmpdir):
        tmpdir.join("setup.py").write(SETUP)
        tmpdir.join("pyproject.toml").write(PYPROJECT)
        dist = self._collect(tmpdir, req=Requirement.from_source(tmpdir))
        assert {"zzz"} == dist.depends.build
