import copy
import logging
from setuptools import sandbox

import pkg_resources

from munch import Munch

from property_manager import cached_property

from . import collectors
from .base import Base
from .config import cfg

log = logging.getLogger(__name__)


class Distribution(Base, pkg_resources.Distribution):

    MULTI_KEYS = (
        "classifier",
        "obsoletes",
        "obsoletes_dist",
        "platform",
        "project_url",
        "provides",
        "provides_dist",
        "provides_extra",
        "requires",
        "requires_dist",
        "requires_external",
        "supported_platform",
    )

    def __init__(self, **kwargs):
        metadata = Munch(
            requires_dist=set(),
            provides_extra=set(),
            extensions=Munch(distinfo=Munch()),
        )
        metadata.update(kwargs)
        super().__init__(metadata=metadata, project_name=metadata.get("name"))

    def __str__(self):
        return super().__str__().replace(" ", "-")

    @classmethod
    def from_req(cls, req):
        metadata = dict()
        with sandbox.pushd(req.source_dir):
            source_dir = req.source_dir
            req.source_dir = "."
            req.run_egg_info()
            for key, value in req.pkg_info().items():
                if value == "UNKNOWN":
                    continue
                key = key.lower().replace("-", "_")
                if key == "keywords":
                    value = sorted(value.split())
                if key in cls.MULTI_KEYS:
                    metadata.setdefault(key, set()).add(value)
                else:
                    metadata[key] = value
            req.source_dir = source_dir
        dist = cls(**metadata)
        # other requirements
        for name in cfg.collectors:
            getattr(collectors, name)(dist, req.source_dir, req=req).collect()
        return dist

    @property
    def metadata(self):
        return self._provider

    @property
    def ext(self):
        return self.extensions.distinfo

    def add_requirement(self, req, extra="run"):
        if extra != "run":
            self.provides_extra.add(extra)
            req = "%s; extra == '%s'" % (req, extra)
        self.requires_dist.add(req)
        del self.reqs
        del self.depends

    @cached_property
    def reqs(self):
        from .requirement import Requirement
        return set(map(Requirement.from_req, self.requires_dist))

    @cached_property
    def depends(self):
        reqs = set(map(copy.deepcopy, self.reqs))
        depends = Munch()
        run = set(filter(lambda r: r.markers is None, self.reqs))
        if run:
            depends["run"] = run
            reqs -= run
        for extra in self.provides_extra:
            depends[extra] = set(map(
                # take the marker off the requirement
                lambda r: setattr(r.req, "marker", None) or r,
                # pylint: disable=cell-var-from-loop
                filter(lambda r: r.markers.evaluate(dict(extra=extra)), reqs)
            ))
        return depends

    # for compatibility with pkg_resources
    @property
    def _dep_map(self):
        depends = self.depends.copy()
        depends[None] = depends.pop("run", [])
        return depends
