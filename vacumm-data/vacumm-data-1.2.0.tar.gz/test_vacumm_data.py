import os
import pytest

from vacumm_data import get_vacumm_data_dir, get_vacumm_data_file


@pytest.mark.parametrize("root", ["user", "system", "egg", "/my/root", None])
def test_get_vacumm_data_dir_roots(root):
    path = get_vacumm_data_dir(check=False, roots=root)
    assert path.endswith(os.path.join('share', 'vacumm'))


def test_get_vacumm_data_dir_envvar():
    mypath = '/my/home/data/vacumm'
    os.environ['VACUMM_DATA_DIR'] = mypath
    path = get_vacumm_data_dir(check=False)
    assert path == mypath
    del os.environ['VACUMM_DATA_DIR']


def test_installed():
    assert get_vacumm_data_dir(check=True) is not None
    assert get_vacumm_data_file('samples/menor.nc', check=True) is not None
