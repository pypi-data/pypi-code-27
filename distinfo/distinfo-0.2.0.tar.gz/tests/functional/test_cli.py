import json

from click.testing import CliRunner

from distinfo import cli

from .cases import Case

SETUP = """
from setuptools import setup
setup(
    name="test.dist",
    install_requires=["xxx"],
)
"""


class TestCli(Case):

    def _invoke(self, tmpdir, *args, **kwargs):
        exit_code = kwargs.pop("exit_code", 0)
        kwargs.setdefault("catch_exceptions", False)
        self._write_setup(tmpdir, SETUP)
        runner = CliRunner()
        result = runner.invoke(cli.main, map(str, args + (tmpdir,)), **kwargs)
        assert result.exit_code == exit_code
        return result

    def test_main_extract(self, tmpdir):
        result = self._invoke(tmpdir, "-c")
        print(result.output)
        # FIXME: logging writes to stdout
        # dist = json.loads(result.output)
        # assert dist["name"] == "test.dist"
        assert "test.dist" in result.output

    def test_main_extract_write(self, tmpdir):
        out = tmpdir.join("out.json")
        self._invoke(tmpdir, "-p", "-o", out)
        dist = json.load(open(out))
        assert dist["name"] == "test.dist"

    def test_main_extract_write_include_exclude(self, tmpdir):
        out = tmpdir.join("out.json")
        self._invoke(tmpdir, "-o", out, "--include=name", "--exclude=name")
        dist = json.load(open(out))
        assert not dist

    def test_main_requires(self, tmpdir):
        result = self._invoke(tmpdir, "-r")
        print(result.output)
        # dist = json.loads(result.output)
        # assert dist["name"] == "test.dist"
        assert "xxx" in result.output

    def test_main_interactive(self, monkeypatch, tmpdir):
        monkeypatch.setattr(cli.repl, "embed", lambda *a, **k: True)
        self._invoke(tmpdir, "-i")
