import pytest

from galacteek.core import jsonf

class File1(jsonf.QJSONFile):
    def prepare(self, root):
        root['comments'] = {
            '1': 'This is it',
        }

@pytest.fixture
def jfile1(tmpdir):
    return File1(tmpdir.join('jsonf1.json'))

class TestMarks:
    def test_simple(self, jfile1):
        jfile1.save()
        print(jfile1.root)
