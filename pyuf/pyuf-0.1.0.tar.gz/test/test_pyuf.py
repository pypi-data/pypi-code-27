import pytest

from pyuf import Partition, UnionFindSpace


@pytest.fixture
def space():
    return UnionFindSpace(
        Partition("letters", "abcdef"),
        Partition("numbers", range(5)),
    )


def test_find(space):
    assert space.find("a") == "letters"
    assert space.find(1) == "numbers"


def test_union(space):
    new_partition = space.union("letters", "numbers")
    expected = "letters_numbers"

    assert new_partition.name == expected
    assert space.find("b") == expected
    assert space.find(3) == expected


def test_union_custom_name(space):
    partition = space.union("letters", "numbers", "alpha")
    assert partition.name == "alpha"


def test_find_then_union(space):
    assert space.find("a") == "letters"
    assert space.find(1) == "numbers"

    space.union("letters", "numbers", "a")

    assert space.find("a") == "a"
    assert space.find(1) == "a"


def test_spacing_decreases(space):
    assert len(space) == 2
    space.union("letters", "numbers")
    assert len(space) == 1
