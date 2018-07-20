from munch import Munch

from setuptools import sandbox

from distinfo.distribution import Distribution
from distinfo.collectors.collector import Collector, PackageCollector

from ..cases import Case


class XCollector(PackageCollector):  # pylint: disable=abstract-method

    name = "testpkg"


class TestCollector(Case):

    def test_add_requirements_file(self, tmpdir):
        requirements = "requirements.txt"
        tmpdir.join(requirements).write("aaa")
        dist = Distribution()
        collector = Collector(dist)
        with sandbox.pushd(tmpdir):
            collector.add_requirements_file(requirements, "run")
            collector.add_requirements_file(requirements, "run")
        assert {"aaa"} == dist.requires.run

    def test_package_collector_run(self):
        dist = Distribution(name="xxx")
        dist.ext.imports = Munch(xxx={XCollector.name})
        dist.ext.packages = ["xxx"]
        collector = XCollector(dist)
        collector.collect()
        assert {XCollector.name} == dist.requires.run

    def test_package_collector_test(self):
        dist = Distribution(name="xxx")
        dist.ext.imports = Munch(tests={XCollector.name})
        dist.ext.packages = ["xxx", "tests"]
        collector = XCollector(dist)
        collector.collect()
        assert {XCollector.name} == dist.requires.test

    def test_package_collector_self(self):
        dist = Distribution(name=XCollector.name)
        collector = XCollector(dist)
        collector.collect()
        assert not dist.requires
