from .collector import Collector


class Git(Collector):

    def _collect(self):
        self.ext.git = (self.path / ".git").exists()
