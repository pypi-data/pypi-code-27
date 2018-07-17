import configparser
import logging
from pathlib import Path
from setuptools import sandbox

from pip._internal.req import parse_requirements

from ..base import Base

log = logging.getLogger(__name__)


class Collector(Base):

    def __init__(self, dist, source_dir, req=None):
        self.dist = dist
        self.source_dir = source_dir
        self.req = req
        self._seen_files = set()

    def __str__(self):
        return str(self.dist)

    def _collect(self):
        raise NotImplementedError()

    def collect(self):
        with sandbox.pushd(self.source_dir):
            self._collect()

    def add_requirement(self, req, extra="test"):
        log.debug("%r %s add %r", self, extra, req)
        self.dist.add_requirement(req, extra=extra)

    def add_requirements_file(self, path):
        if path in self._seen_files:
            log.warning("%r already seen %r", self, path)
            return
        self._seen_files.add(path)
        for req in parse_requirements(path, session=True):
            self.add_requirement(req.req)

    def get_setup_cfg(self):
        setup = Path("setup.cfg")
        if setup.exists():
            config = configparser.ConfigParser()
            config.read(setup)
            return config


class PackageCollector(Collector):

    name = None

    def _collect(self):
        if getattr(self.dist, "name", None) == self.name:
            return
        req = self._requires()
        if req:
            self.add_requirement(req)
