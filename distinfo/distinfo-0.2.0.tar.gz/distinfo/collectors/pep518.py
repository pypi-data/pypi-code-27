import logging

import pytoml

from .. import util
from .collector import Collector

log = logging.getLogger(__name__)


class Pep518(Collector):

    PYPROJECT = "pyproject.toml"

    def _collect(self):
        pyproject = self.path / self.PYPROJECT
        if pyproject.exists():
            toml = pytoml.load(pyproject.open())
            # pep 518
            for req in util.dotget(toml, "build-system.requires", []):
                self.add_requirement(req, "build")
            # flit: http://flit.readthedocs.io/en/latest/pyproject_toml.html
            # FIXME: incomplete
            for req in util.dotget(toml, "tool.flit.metadata.requires", []):
                self.add_requirement(req, "run")
            for req in util.dotget(toml, "tool.flit.metadata.dev-requires", []):
                self.add_requirement(req, "dev")
