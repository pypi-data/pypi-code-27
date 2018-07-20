from .collector import PackageCollector


class Nose(PackageCollector):

    name = "nose"

    def _requires(self):
        if (self.path / ".noserc").exists():
            return self.name
