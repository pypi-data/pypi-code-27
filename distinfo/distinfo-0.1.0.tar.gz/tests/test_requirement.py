from distinfo import Requirement

from .cases import TestCase


class TestRequirement(TestCase):

    def test_repr(self):
        req = Requirement.from_req("xxx")
        assert "Requirement xxx" in repr(req)

    def test_eq(self):
        req = Requirement.from_req("xxx")
        req2 = Requirement.from_req("xxx")
        req3 = Requirement.from_req("yyy>1")
        assert req == req2
        assert req != req3
        assert req == "xxx"
        assert req != "yyy"
        assert req3 == "yyy"
