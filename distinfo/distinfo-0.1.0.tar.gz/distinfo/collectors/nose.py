from pathlib import Path

from .collector import PackageCollector


class Nose(PackageCollector):

    name = "nose"

    def _requires(self):
        if Path(".noserc").exists():
            return self.name
