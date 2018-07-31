"""
Tests for sumndx.

The tests are meant to be run using pytest. They assume the following file
tree::

    sumndx/
    ├── LICENSE.txt
    ├── README.md
    ├── setup.cfg
    ├── setup.py
    ├── sumndx
    └── tests
        └── test_sumndx.py

To run the tests, move to the "tests" directory and run::

    pytest

"""

from contextlib import redirect_stdout
from pathlib import Path
import imp
import io

import pytest

# The sumndx script does not have the .py file extension. It therefore cannot
# be imported whith a regular import. It can still be imported, though, as we
# know where the file is. We assume that the "sumndx" script and the test
# directory are at the same level. See the module docstring for the assumed
# file tree.
_test_directory = Path(__file__).parent
_data_directory = _test_directory / 'data'
_sumndx_path = _test_directory / '../sumndx'
sumndx = imp.load_source('sumndx', str(_sumndx_path))


OUTPUT_REFERENCE = '''\
0\tSystem\t200
1\tGroup 1\t10
2\tOther group\t1
'''


def test_main_help():
    """
    Test that calling the help exits the program.
    """
    with pytest.raises(SystemExit):
        sumndx.main(['sumndx', '-h'])


def test_main_unfound_file():
    """
    Make sure the program exits when given an non existing file.
    """
    with pytest.raises(SystemExit):
        sumndx.main(['sumndx', 'unfound.ndx'])


@pytest.mark.parametrize('file_path, output_ref', (
    (_data_directory / 'simple.ndx', OUTPUT_REFERENCE),
    (_data_directory / 'spaces.ndx', OUTPUT_REFERENCE),
    (_data_directory / 'comments.ndx', OUTPUT_REFERENCE),
))
def test_main(file_path, output_ref):
    """
    Test that the output is what is expected.
    """
    output = io.StringIO()
    with redirect_stdout(output):
        sumndx.main(['sumndx', str(file_path)])
    output_str = output.getvalue()
    assert output_str == output_ref
