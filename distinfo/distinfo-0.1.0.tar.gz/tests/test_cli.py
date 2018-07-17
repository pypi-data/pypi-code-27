# import json

from click.testing import CliRunner

from distinfo import cli

from .cases import TestCase


class TestCli(TestCase):

    def _invoke(self, *args, **kwargs):
        exit_code = kwargs.pop("exit_code", 0)
        runner = CliRunner()
        kwargs.setdefault("catch_exceptions", False)
        result = runner.invoke(*args, **kwargs)
        assert result.exit_code == exit_code
        return result

    def test_main_extract(self):
        result = self._invoke(cli.main, ["-c", str(self.data_path / "test.dist")])
        print(result.output)
        # FIXME: log output gets written to stdout
        # dist = json.loads(result.output)
        # assert dist["name"] == "test.dist"
        assert "test.dist" in result.output

    def test_main_depends(self):
        result = self._invoke(cli.main, ["-d", str(self.data_path / "test.dist")])
        print(result.output)
        # dist = json.loads(result.output)
        # assert dist["name"] == "test.dist"
        assert "xxx" in result.output

    def test_main_interactive(self, monkeypatch):
        monkeypatch.setattr(cli.repl, "embed", lambda *a, **k: True)
        self._invoke(cli.main, ["-i"])
