from .collector import PackageCollector


class Pytest(PackageCollector):

    name = "pytest"

    def _requires(self):

        # look for setup.cfg section
        config = self._get_setup_cfg()
        if config is not None:
            for key in ("pytest", "tool:pytest"):
                if key in config:
                    addopts = config[key].get("addopts", "")
                    if "--cov" in addopts:
                        return "pytest-cov"
                    return self.name

        # look for conftest.py files
        conftest = list(self.path.glob("**/conftest.py"))
        if conftest:
            return self.name
