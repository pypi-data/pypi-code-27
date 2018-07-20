from pipreqs import pipreqs

from distinfo.collectors.pipreqs import PipReqs

from .cases import Case

PACKAGE = """
import aaa
import ccc
"""

TESTS = """
import xxx
import bbb
"""


class TestPipReqs(Case):

    collector = PipReqs

    def test_collect(self, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write(PACKAGE)
        tmpdir.join("tests").mkdir().join("__init__.py") .write(TESTS)
        collector = self._collect(
            tmpdir,
            name="xxx",
            packages=["xxx", "tests"],
            tests=["tests"],
            reqs=["ccc"],
        )
        assert collector.ext.imports.xxx == {"aaa", "ccc"}
        assert collector.ext.imports.tests == {"bbb"}

    def test_collect_empty(self, tmpdir):
        collector = super().test_collect_empty(tmpdir)
        assert not hasattr(collector.ext, "imports")

    def test_collect_fail(self, monkeypatch, tmpdir):
        tmpdir.join("xxx").mkdir().join("__init__.py") .write("import aaa")
        monkeypatch.setattr(pipreqs, "get_pkg_names", self._raiser())
        collector = self._collect(tmpdir, packages=["xxx"])
        assert not collector.ext.imports
