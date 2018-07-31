"""
Unit and regression test for the cc_example package.
"""

# Import package, test suite, and other packages as needed
import cc_example
import pytest
import sys

def test_cc_example_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "cc_example" in sys.modules
