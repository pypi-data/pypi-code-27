import io

import pytest

from distinfo import util

from .cases import TestCase


class TestUtil(TestCase):

    @pytest.mark.parametrize("fmt", util.DUMPERS.keys())
    def test_dump(self, fmt):
        obj = dict(
            one=set(),
            two=2,
        )
        stream = io.StringIO()
        util.dump(obj, fmt=fmt, file=stream)
        assert "one" in stream.getvalue()
