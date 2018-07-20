import importlib
import logging
import os
import sys

from munch import DefaultMunch, Munch

from packaging.markers import InvalidMarker, Marker
from packaging.requirements import InvalidRequirement

from property_manager import cached_property

from setuptools import sandbox

from . import util
from .base import Base
from .config import cfg
from .requirement import Requirement

log = logging.getLogger(__name__)


class Distribution(Base):

    BUILD_IMPLICIT = ("setuptools", "wheel")

    def __init__(self, path=None, **kwargs):
        self.path = path
        self.metadata = Munch(
            name="UNKNOWN",
            version="0.0.0",
            provides_extra=set(),
            requires_dist=set(),
            extensions=Munch(distinfo=Munch()),
        )
        self.metadata.update(kwargs)
        if self.path is not None:
            self.path = os.path.relpath(self.path)
            with sandbox.pushd(self.path), sandbox.save_path():
                sys.path.insert(0, ".")
                for name in cfg.collectors:
                    module = importlib.import_module(
                        "distinfo.collectors.%s" % name.lower()
                    )
                    getattr(module, name)(self).collect()
        # a side effect of the below is that `requires` will remove any invalid
        # requirements
        if self.requires:
            log.debug(
                "%r requires:\n%s",
                self,
                util.dumps(self.requires, fmt="yamls"),
            )

    def __str__(self):
        return "%s-%s%s" % (
            self.name,
            self.version,
            self.path and " path=%s" % self.path or "",
        )

    @property
    def name(self):
        return self.metadata.name

    @name.setter
    def name(self, name):
        self.metadata.name = name

    @property
    def version(self):
        return self.metadata.version

    @property
    def provides_extra(self):
        return self.metadata.provides_extra

    @property
    def requires_dist(self):
        return self.metadata.requires_dist

    @property
    def ext(self):
        return self.metadata.extensions.distinfo

    def _filter_reqs(self, reqs, extra):
        filtered = set()
        env = dict(extra=extra)
        for req in reqs:
            if extra == "run":
                if req.marker is None or req.marker.evaluate(env):
                    filtered.add(req)
            else:
                if req.marker is not None and req.marker.evaluate(env):
                    filtered.add(req)
        return filtered

    @cached_property
    def requires(self):
        reqs = set()
        for req in self.requires_dist:
            try:
                req = Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r requirement %r raised: %r", self, req, exc)
                self.requires_dist.remove(req)
            else:
                reqs.add(req)
        requires = DefaultMunch(set())
        run = self._filter_reqs(reqs, "run")
        if run:
            requires["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            ereqs = self._filter_reqs(reqs, extra)
            if ereqs:
                requires[extra] = ereqs
        return requires

    def add_requirement(self, req, extra="run"):

        # cast to Requirement
        if isinstance(req, str):
            try:
                req = Requirement(req)
            except InvalidRequirement as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
        else:
            # belt and braces
            assert isinstance(req, Requirement)

        # skip out for implicit build requirements
        if extra == "build" and req in self.BUILD_IMPLICIT:
            return

        # skip out if requirement is already present
        if req in self.requires[extra] \
                or (extra != "run" and req in self.requires["run"]):
            return

        if extra != "run":
            self.provides_extra.add(extra)
            # set marker
            try:
                marker = Marker(extra[1:] if extra.startswith(":")
                                else "extra == '%s'" % extra)
            except InvalidMarker as exc:
                log.warning("%r %r add %r raised %r", self, extra, req, exc)
                return
            if req.marker is not None:
                marker = Marker("(%s) and %s" % (req.marker, marker))
            req.marker = marker

        self.requires_dist.add(str(req))
        del self.requires
        return req
