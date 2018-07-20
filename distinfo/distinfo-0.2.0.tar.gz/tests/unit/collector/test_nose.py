from distinfo.collectors.nose import Nose

from .cases import Case


class TestNose(Case):

    collector = Nose

    def test_collect(self, tmpdir):
        tmpdir.join(".noserc").write("x")
        collector = self._collect(tmpdir)
        assert {"nose"} == collector.requires.test
