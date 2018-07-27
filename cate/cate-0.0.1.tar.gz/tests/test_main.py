# -*- coding: utf-8 -*-

import io

import pytest

from cate import main


# pylint: disable=missing-docstring
class TestLoad:
    VALID_TESTCASES = {
        'valid_matrix_missing_coeff': '[[0, 0], [0]]',
        'valid_matrix': '[[1, 1], [1, 2]]',
    }
    FAILING_TESTCASES = {
        'malformed_json_empty': '',
        'malformed_json_missing_closing_bracket': '[',
        'malformed_json_extra_comma': '[[0, 0], [0, 0],]',
        'invalid_matrix_None': 'null',
        'invalid_matrix_boolean': 'true',
        'invalid_matrix_empty': '[]',
        'invalid_matrix_dict': '{"super": "matrix"}',
        'invalid_matrix_string_coeff': '[["1", 0], [0, 1]]',
        'invalid_matrix_float_coeff': '[[1.0, 0], [0, 1]]',
        'invalid_matrix_list_of_dict': '[{}]',
    }

    @staticmethod
    def build_valid_test(input_):
        def _valid_test(_):
            fp = io.StringIO(input_)  # pylint: disable=invalid-name
            # check no exception is raised
            main._load_matrix_from_input(fp)  # pylint: disable=protected-access
        return _valid_test

    @staticmethod
    def build_failing_test(input_):
        def _failing_test(_):
            fp = io.StringIO(input_)  # pylint: disable=invalid-name
            with pytest.raises(TypeError):
                main._load_matrix_from_input(fp)  # pylint: disable=protected-access
        return _failing_test


# actually bind testcases to class' methods
for name, json in TestLoad.VALID_TESTCASES.items():
    setattr(TestLoad, 'test_' + name, TestLoad.build_valid_test(json))
for name, json in TestLoad.FAILING_TESTCASES.items():
    setattr(TestLoad, 'test_' + name, TestLoad.build_failing_test(json))
