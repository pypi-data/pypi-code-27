from distinfo.collectors.findtests import FindTests

from .cases import Case


class TestFindTests(Case):

    collector = FindTests

    def test_collect(self, tmpdir):
        tmpdir.join("test.py").write("True")
        collector = self._collect(tmpdir)
        assert collector.ext.tests

    def test_collect_empty(self, tmpdir):
        collector = super().test_collect_empty(tmpdir)
        assert not hasattr(collector.ext, "tests")
