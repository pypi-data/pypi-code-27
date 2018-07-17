from distinfo.collectors import Nose

from .cases import TestCase


class TestNose(TestCase):

    collector = Nose

    def test_collect(self, tmpdir):
        tmpdir.join(".noserc").write("x")
        dist = self._collect(tmpdir)
        assert {"nose"} == dist.depends.test
