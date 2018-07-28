import pytest


def bar():
    import pdb; pdb.set_trace()


def foo():
    bar()


def test_pdb():
    foo()


class TestClasses():
    @pytest.mark.parametrize("food", ['ham', 'egg'])
    def test_class_pdb(self, food):
        foo()
