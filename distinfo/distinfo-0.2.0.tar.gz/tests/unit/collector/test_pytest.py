from distinfo.collectors.pytest import Pytest

from .cases import Case

SETUPCFG = """
[tool:pytest]
addopts = -v
"""

SETUPCFG_COV = """
[tool:pytest]
addopts = --cov
"""


class TestPytest(Case):

    collector = Pytest

    def test_collect_conftest(self, tmpdir):
        tmpdir.join("conftest.py").write("True")
        collector = self._collect(tmpdir)
        assert {"pytest"} == collector.requires.test

    def test_setupcfg(self, tmpdir):
        tmpdir.join("setup.cfg").write(SETUPCFG)
        collector = self._collect(tmpdir)
        assert {"pytest"} == collector.requires.test

    def test_setupcfg_cov(self, tmpdir):
        tmpdir.join("setup.cfg").write(SETUPCFG_COV)
        collector = self._collect(tmpdir)
        assert {"pytest-cov"} == collector.requires.test

    def test_setupcfg_none(self, tmpdir):
        tmpdir.join("setup.cfg").write("")
        collector = self._collect(tmpdir)
        assert not collector.requires
