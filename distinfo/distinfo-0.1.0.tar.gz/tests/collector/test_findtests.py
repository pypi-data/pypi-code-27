from distinfo.collectors import FindTests

from .cases import TestCase


class TestFindTests(TestCase):

    collector = FindTests

    def test_collect(self, tmpdir):
        tmpdir.join("test.py").write("True")
        dist = self._collect(tmpdir)
        assert dist.ext.tests

    def test_collect_false(self, tmpdir):
        dist = self._collect(tmpdir)
        assert not dist.ext.tests
