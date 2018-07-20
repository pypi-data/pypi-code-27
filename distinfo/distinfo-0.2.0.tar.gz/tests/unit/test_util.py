import io

import pytest

from distinfo import util

from .cases import Case


class TestUtil(Case):

    @pytest.mark.parametrize("fmt", list(util.DUMPERS.keys()))
    def test_dump(self, fmt):
        obj = dict(
            one=set(),
            two=2,
            three=dict(x=1),
        )
        stream = io.StringIO()
        util.dump(obj, fmt=fmt, file=stream)
        assert "one" in stream.getvalue()
