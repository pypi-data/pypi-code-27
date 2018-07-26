from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from typhoon.utils import NoDuplicatesDict

from typhoon.license_typhoontest.manager import lic_check


# Check for license everytime typhoon.test is imported
lic_check()


def check_if_internal_capture(signal):
    if isinstance(signal, str):
        if capture is None:
            raise ValueError("Signal given as a string but there is no past captured data available yet.")
        else:
            signal = capture[signal]
    return signal

capture = None
marks = NoDuplicatesDict()


class wont_raise(object):
    """Used as a context manager where we don't expect any exception do be raised.
    Pytest still does not provide this out-of-the-box because of disagreements on naming.
    See: https://github.com/pytest-dev/pytest/issues/1830
    """
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, *excinfo):
        pass

