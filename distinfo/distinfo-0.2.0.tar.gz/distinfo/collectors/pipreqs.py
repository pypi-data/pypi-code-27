import logging

from munch import Munch

from pipreqs import pipreqs

from ..config import cfg
from .collector import Collector

log = logging.getLogger(__name__)


class PipReqs(Collector):

    IGNORE = (
        "setuptools",
    )

    def _get_packages(self, path):
        try:
            return set(
                filter(
                    lambda p: p != self.dist.name and p not in self.IGNORE,
                    map(
                        lambda p: cfg.package_aliases.get(p, p),
                        map(
                            str.lower,
                            pipreqs.get_pkg_names(pipreqs.get_all_imports(path)),
                        )
                    )
                )
            )
        except Exception as exc:
            self._warn_exc(exc)
            return set()

    def _collect(self):
        self.ext.imports = Munch()
        packages = getattr(self.ext, "packages", [])
        for package in packages:
            self.ext.imports[package] = self._get_packages(package) - {self.dist.name}
