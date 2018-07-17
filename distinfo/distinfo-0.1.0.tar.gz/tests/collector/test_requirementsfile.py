from distinfo.collectors import RequirementsFile

from .cases import TestCase


class TestRequirementsFile(TestCase):

    collector = RequirementsFile

    def test_collect(self, tmpdir):
        tmpdir.join("requirements-test.txt").write("aaa")
        dist = self._collect(tmpdir)
        assert {"aaa"} == dist.depends.test
