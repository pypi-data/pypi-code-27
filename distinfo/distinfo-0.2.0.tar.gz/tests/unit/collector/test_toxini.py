from tox.exception import ConfigError

from distinfo.collectors import toxini

from .cases import Case

TOXINI = """
[tox]
envlist = py27, pypy, py34, py35, py36, py37

[testenv]
deps =
    zzz
    -r requirements.txt
    -r requirements-missing.txt
    -c xxx
commands =
    pip install xxx
    python -m pytest
    - false
setenv =
    ONE = 1
"""

REQUIREMENTS = """
# comment

aaa
"""

TOXINI_BAD = """
[tox]
envlist = xxx
"""


class TestRequirementsFile(Case):

    collector = toxini.ToxIni

    def test_collect(self, caplog, tmpdir):
        tmpdir.join("tox.ini").write(TOXINI)
        tmpdir.join("requirements.txt").write(REQUIREMENTS)
        collector = self._collect(tmpdir)
        assert {"aaa", "zzz"} == collector.requires.test
        assert ["python -m pytest", "false || true"] == collector.ext.tox.commands
        assert collector.ext.tox.env.ONE == "1"
        assert "ignoring command" in caplog.text

    def test_collect_bad(self, tmpdir):
        tmpdir.join("tox.ini").write(TOXINI_BAD)
        collector = self._collect(tmpdir)
        assert not collector.requires

    def test_collect_conf_error(self, monkeypatch, tmpdir):
        monkeypatch.setattr(toxini, "parseconfig", self._raiser(ConfigError))
        tmpdir.join("tox.ini").write(TOXINI)
        collector = self._collect(tmpdir)
        assert not collector.requires
