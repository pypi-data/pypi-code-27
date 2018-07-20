from distinfo import const
from distinfo.collectors import distinfo

from .cases import Case

SETUP = """
from setuptools import setup
setup(
    # this needs to be present or distutils barfs
    setup_requires=["setuptools"],
    install_requires=["bbb"],
    # badly specified requirements, seen in unittest2
    tests_require=(["ccc"],),
    extras_require=dict(test="ddd"),
)
"""


class TestDistInfo(Case):

    collector = distinfo.DistInfo

    def test_collect(self, tmpdir):
        self._write_setup(tmpdir, SETUP)
        tmpdir.join("xxx").mkdir().join("__init__.py").write("")
        collector = self._collect(tmpdir)
        assert not collector.requires.build
        assert {"bbb"} == collector.requires.run
        assert {"ccc", "ddd"} == collector.requires.test
        assert ["xxx"] == collector.ext.packages

    def test_process_output(self, tmpdir):
        collector = self._collect(tmpdir)
        collector._process_output("Searching for xxx")
        assert collector.requires.build == {"xxx"}

    def test_collect_empty(self, caplog, tmpdir):  # pylint: disable=arguments-differ
        super().test_collect_empty(tmpdir)
        assert "has no %s" % const.SETUP_PY in caplog.text

    def test_run_dist_info_fail(self, caplog, monkeypatch, tmpdir):
        def _raiser(action):
            if action == "dist_info":
                raise Exception()
            return run_setup(action)
        run_setup = distinfo.run_setup
        monkeypatch.setattr(distinfo, "run_setup", _raiser)
        self._write_setup(tmpdir, SETUP)
        collector = self._collect(tmpdir)
        assert "dist_info raised" in caplog.text
        assert collector.name == "UNKNOWN"

    def test_run_egg_info_fail(self, caplog, monkeypatch, tmpdir):
        monkeypatch.setattr(distinfo, "run_setup", self._raiser())
        self._write_setup(tmpdir, SETUP)
        collector = self._collect(tmpdir)
        assert "egg_info raised" in caplog.text
        assert collector.name == "UNKNOWN"
