import logging

import requirementslib

from .collector import Collector

log = logging.getLogger(__name__)


class Pipfile(Collector):

    EXTRAS = {
        "packages": "run",
        "dev-packages": "dev",
    }

    def _collect(self):
        if (self.path / "Pipfile").exists():
            try:
                pipfile = requirementslib.Pipfile.load(".")
                sections = pipfile.get_sections()
                for section, extra in self.EXTRAS.items():
                    packages = sections.get(section) or {}
                    for name, spec in packages.items():
                        if spec == "*":
                            spec = ""
                        self.add_requirement("%s%s" % (name, spec), extra)
            except Exception as exc:
                self._warn_exc(exc)
