from collections import defaultdict
import logging

from setuptools import distutils, sandbox

from ..exc import DistInfoException
from .collector import Collector

log = logging.getLogger(__name__)


class Distutils(Collector):

    # map distutils.core.Distribution attrs to extra names
    EXTRAS = dict(
        setup_requires="build",
        install_requires="run",
        tests_require="test",
    )

    def _collect(self):
        # pylint: disable=protected-access

        # run setup.py to populate `distutils.core._setup_distribution`
        distutils.core._setup_distribution = None
        distutils.core._setup_stop_after = "config"
        argv = ("setup.py", "-h")
        with sandbox.save_argv(argv):
            try:
                sandbox._execfile(
                    argv[0],
                    dict(__file__=argv[0], __name__="__main__"),
                )
            except BaseException as exc:
                msg = "%r raised %r" % (argv, exc)
                if distutils.core._setup_distribution is None:
                    raise DistInfoException(msg)
                log.warning(msg)
        dist = distutils.core._setup_distribution
        assert dist is not None, "distutils.core.setup not called"

        # take requirements from dist
        requires = defaultdict(set)
        requires.update(
            {k: set(v) for k, v in getattr(dist, "extras_require", {}).items()}
        )
        for attr, extra in self.EXTRAS.items():
            reqs = getattr(dist, attr, None)
            requires[extra] |= set(reqs or [])
        for extra, reqs in requires.items():
            for req in reqs:
                self.add_requirement(req, extra=extra)
