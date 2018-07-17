from setuptools import sandbox

from distinfo import Distribution
from distinfo.collectors.collector import Collector, PackageCollector

from ..cases import TestCase


class XCollector(PackageCollector):
    name = "xxx"


class TestPytest(TestCase):

    def test_add_requirements_file(self, tmpdir):
        requirements = "requirements.txt"
        tmpdir.join(requirements).write("aaa")
        dist = Distribution()
        collector = Collector(dist, tmpdir)  # pylint: disable=not-callable
        with sandbox.pushd(tmpdir):
            collector.add_requirements_file(requirements)
            collector.add_requirements_file(requirements)
        assert {"aaa"} == dist.depends.test

    def test_package_collector(self, tmpdir):
        dist = Distribution(name="xxx")
        collector = XCollector(dist, tmpdir)  # pylint: disable=not-callable
        collector.collect()
        assert not dist.depends
