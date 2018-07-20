import distutils.core
from email.parser import FeedParser
import logging
import re

import capturer

from munch import Munch

from setuptools import sandbox

from .. import const
from .collector import Collector

log = logging.getLogger(__name__)

SEARCH_PATTERN = re.compile("Searching for (.*)")


# run_setup from distutils.core doesn't work in every case - this does
def run_setup(action):
    distutils.core._setup_distribution = None
    with sandbox.save_argv((const.SETUP_PY, action)):
        sandbox._execfile(
            const.SETUP_PY,
            dict(__file__=const.SETUP_PY, __name__="__main__"),
        )
    dist = distutils.core._setup_distribution
    assert dist is not None, "distutils.core.setup not called"
    return dist


class DistInfo(Collector):

    MULTI_KEYS = (
        "classifier",
        "obsoletes_dist",
        "platform",
        "project_url",
        "provides_dist",
        "provides_extra",
        "requires_dist",
        "requires_external",
        "supported_platform",
    )

    # these are from PEP 314 Metadata 1.1
    KEY_ALIASES = dict(
        obsoletes="obsoletes_dist",
        provides="provides_dist",
        requires="requires_dist",
    )

    def _process_output(self, output):
        for req in SEARCH_PATTERN.findall(output):
            self.add_requirement(req, "build")

    def _collect(self):

        if not (self.path / const.SETUP_PY).exists():
            log.warning("%r has no %s", self, const.SETUP_PY)
            return

        warnings = []
        try:
            with capturer.CaptureOutput(relay=False) as capture:
                try:
                    dist = run_setup("dist_info")
                except BaseException as exc:
                    warnings.append("%r dist_info raised %r" % (self, exc))
                    try:
                        dist = run_setup("egg_info")
                    except BaseException as exc:
                        warnings.append("%r egg_info raised %r" % (self, exc))
                        return
        finally:
            for warning in warnings:
                log.warning(warning)
            self._process_output(capture.get_text())

        # get metadata
        provides_dist = True
        infos = list(self.path.glob("**/*.dist-info/METADATA"))
        if not infos:
            provides_dist = False
            infos = list(self.path.glob("**/*.egg-info/PKG-INFO"))
        assert infos
        parser = FeedParser()
        parser.feed(open(infos[0]).read())
        message = parser.close()
        for key, value in message.items():
            value = value.strip()
            if not value or value == "UNKNOWN":
                continue
            key = key.lower().replace("-", "_")
            key = self.KEY_ALIASES.get(key, key)
            if key in self.MULTI_KEYS:
                self.metadata.setdefault(key, set()).add(value)
            else:
                self.metadata[key] = value

        # get requirements from distutils dist
        extras = Munch(setup_requires="build", tests_require="test")
        if not provides_dist:
            extras.install_requires = "run"
            for extra, reqs in getattr(dist, "extras_require", {}).items():
                for req in reqs:
                    self.add_requirement(req, extra)
        for attr, extra in extras.items():
            reqs = getattr(dist, attr, None) or []
            # fix incorrectly specified requirements (unittest2 does this)
            if isinstance(reqs, tuple) and isinstance(reqs[0], list):
                reqs = reqs[0]
            for req in reqs:
                self.add_requirement(req, extra)

        # get packages
        self.ext.packages = list(map(
            lambda p: str(p.parent.relative_to(".")),
            sorted(self.path.glob("*/__init__.py")),
        ))
