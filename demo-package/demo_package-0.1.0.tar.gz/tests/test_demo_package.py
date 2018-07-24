#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `demo_package` package."""

import pytest
import os

from click.testing import CliRunner

from demo_package import demo_package
from demo_package import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'demo_package.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_add():
    assert demo_package.add(1, 2, 3) == 6
    assert demo_package.add("1", "2", "3") == "123"
    assert demo_package.add([1], [2, 3], [4, 5, 6]) == [1, 2, 3, 4, 5, 6]

    with pytest.raises(TypeError):
        demo_package.add(1, "a", "c")



testdata = [(1, 2, 3, 6),
            ("1", "2", "3", "123"),
            ([], [], [], []),
            ]
@pytest.mark.parametrize("a,b,c,expected", testdata)
def test_add_multiple(a, b, c, expected):
    assert demo_package.add(a, b, c) == expected


@pytest.fixture
def setup_file(tmpdir):
    path = tmpdir.join("input.txt").strpath
    yield path
    os.remove(path)


@pytest.fixture
def fill_file(setup_file):
    with open(setup_file, "w") as fh:
        print(1, file=fh)
        print(2, file=fh)
        print(3, file=fh)
    yield setup_file


def test_sumup_file(fill_file):
    assert demo_package.sumup_file(fill_file) == 6

