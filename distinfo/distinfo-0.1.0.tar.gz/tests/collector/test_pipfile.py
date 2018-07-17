from distinfo.collectors import Pipfile

from .cases import TestCase

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


class TestPipFile(TestCase):

    collector = Pipfile

    def test_collect(self, tmpdir):
        tmpdir.join("Pipfile").write(PIPFILE)
        dist = self._collect(tmpdir)
        assert {"yyy>=1"} == dist.depends.dev
        assert {"zzz"} == dist.depends.run

    def test_bad_collect(self, tmpdir):
        tmpdir.join("Pipfile").write("xxx")
        self._collect(tmpdir)
