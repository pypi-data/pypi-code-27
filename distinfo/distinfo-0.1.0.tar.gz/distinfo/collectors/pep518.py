from .collector import Collector


class Pep518(Collector):

    def _collect(self):
        reqs, present = self.req.get_pep_518_info()
        if present:
            for req in reqs:
                self.add_requirement(req, extra="build")
