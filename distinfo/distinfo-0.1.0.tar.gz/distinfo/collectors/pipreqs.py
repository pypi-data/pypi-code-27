import logging
from setuptools import find_packages

from munch import Munch

from pipreqs import pipreqs

from ..config import cfg
from .collector import Collector

log = logging.getLogger(__name__)


class PipReqs(Collector):

    def _get_packages(self, path):
        return set(map(
            str.lower,
            pipreqs.get_pkg_names(pipreqs.get_all_imports(path)),
        ))

    def _collect(self):

        imports = Munch()
        toplevel_imports = self._get_packages(".")
        packages = list(filter(lambda p: p.find(".") == -1, find_packages()))

        # check each package
        for package in packages:
            pkg_imports = imports.setdefault(package, set())
            pkg_imports |= self._get_packages(package)
            toplevel_imports -= pkg_imports

        # remove self references
        for pkg_imports in imports.values():
            for package in packages:
                if package in pkg_imports:
                    pkg_imports.remove(package)

        # check dist package
        distpkg = imports.get(self.dist.name)
        if distpkg is not None:
            run = getattr(self.dist.depends, "run", [])
            missing = []
            for pkg in distpkg:
                if cfg.package_aliases.get(pkg, pkg) not in run \
                        and pkg.replace("_", "-") not in run:
                    missing.append(pkg)
            if missing:
                log.warning("%s missing run dependencies: %r", self, missing)
        if toplevel_imports:
            imports["build"] = toplevel_imports
        if imports:
            self.dist.ext.imports = imports
