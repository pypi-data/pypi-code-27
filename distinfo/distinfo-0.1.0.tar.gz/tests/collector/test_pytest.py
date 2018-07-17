from distinfo.collectors import Pytest

from .cases import TestCase

SETUPCFG = """
[tool:pytest]
addopts = -v
"""

SETUPCFG_COV = """
[tool:pytest]
addopts = --cov
"""


class TestPytest(TestCase):

    collector = Pytest

    def test_collect_conftest(self, tmpdir):
        tmpdir.join("conftest.py").write("True")
        dist = self._collect(tmpdir)
        assert {"pytest"} == dist.depends.test

    def test_setupcfg(self, tmpdir):
        tmpdir.join("setup.cfg").write(SETUPCFG)
        dist = self._collect(tmpdir)
        assert {"pytest"} == dist.depends.test

    def test_setupcfg_cov(self, tmpdir):
        tmpdir.join("setup.cfg").write(SETUPCFG_COV)
        dist = self._collect(tmpdir)
        assert {"pytest-cov"} == dist.depends.test

    def test_setupcfg_none(self, tmpdir):
        tmpdir.join("setup.cfg").write("")
        dist = self._collect(tmpdir)
        assert not dist.depends
