import configparser
import logging
from pathlib import Path

from ..base import Base
from ..requirement import Requirement

log = logging.getLogger(__name__)


class Collector(Base):

    def __init__(self, dist):
        self.dist = dist
        self.path = Path()
        self._seen_files = set()

    def __getattr__(self, key):
        return getattr(self.dist, key)

    def __str__(self):
        return str(self.dist)

    def _warn_exc(self, exc):
        log.warning("%r raised %r", self, exc)

    def _collect(self):
        raise NotImplementedError()

    def _clean_dict(self, obj):
        drop = []
        for key, value in obj.items():
            if not isinstance(value, bool) and not value:
                drop.append(key)
            elif isinstance(value, dict):
                self._clean_dict(value)
        for key in drop:
            del obj[key]

    def collect(self):
        assert self.path is not None
        self._collect()
        self._clean_dict(self.ext)

    def add_requirement(self, req, extra):
        req = self.dist.add_requirement(req, extra=extra)
        if req is not None:
            log.debug("%r %r add %r", self, extra, req)

    def add_requirements_file(self, path, extra):
        if path in self._seen_files:
            log.warning("%r already seen %r", self, path)
            return
        self._seen_files.add(path)
        for req in Requirement.parse_file(path):
            self.add_requirement(req, extra)

    def _get_setup_cfg(self):
        setup = self.path / "setup.cfg"
        if setup.exists():
            config = configparser.ConfigParser()
            config.read(setup)
            return config


class PackageCollector(Collector):

    name = None

    def _requires(self):
        raise NotImplementedError()

    def _collect(self):
        if self.dist.name == self.name:
            return
        # check imports for the package name
        req = False
        extra = "test"
        imports = getattr(self.ext, "imports", {})
        for package in getattr(self.ext, "packages", []):
            if self.name in imports.get(package, []):
                req = self.name
                if package == self.dist.name:
                    extra = "run"
                break
        # if not found here then hand off to subclass
        if not req:
            req = self._requires()
        if req:
            self.add_requirement(req, extra)
