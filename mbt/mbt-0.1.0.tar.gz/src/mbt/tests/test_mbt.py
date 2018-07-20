import pytest
import mbt


def test_project_defines_author_and_version():
    assert hasattr(mbt, '__author__')
    assert hasattr(mbt, '__version__')
