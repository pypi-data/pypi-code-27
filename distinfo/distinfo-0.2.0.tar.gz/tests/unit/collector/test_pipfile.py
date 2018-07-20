from distinfo.collectors.pipfile import Pipfile

from .cases import Case

PIPFILE = """
[[source]]
url = "https://pypi.org/simple/"
verify_ssl = true
name = "pypi"

[dev-packages]
"yyy" = ">=1"

[packages]
"zzz" = "*"
"""


class TestPipFile(Case):

    collector = Pipfile

    def test_collect(self, tmpdir):
        tmpdir.join("Pipfile").write(PIPFILE)
        collector = self._collect(tmpdir)
        assert {"yyy"} == collector.requires.dev
        assert {"zzz"} == collector.requires.run

    def test_bad_collect(self, caplog, tmpdir):
        tmpdir.join("Pipfile").write("xxx")
        self._collect(tmpdir)
        assert "raised" in caplog.text
