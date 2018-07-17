from distinfo import Distribution

from ..cases import TestCase as _TestCase


class TestCase(_TestCase):

    collector = None

    def _collect(self, tmpdir, req=None):
        dist = Distribution(name="xxx")
        collector = self.collector(dist, tmpdir, req=req)  # pylint: disable=not-callable
        collector.collect()
        return dist
