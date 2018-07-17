import subprocess

from .collector import PackageCollector


class Pytest(PackageCollector):

    name = "pytest"

    def _requires(self):

        config = self.get_setup_cfg()
        if config is not None:
            for key in ("pytest", "tool:pytest"):
                if key in config:
                    addopts = config[key].get("addopts", "")
                    if "--cov" in addopts:
                        return "pytest-cov"
                    return self.name

        conftest = subprocess.check_output((
            "find",
            ".",
            "-name",
            "conftest.py",
        )).strip()
        if conftest:
            return self.name
