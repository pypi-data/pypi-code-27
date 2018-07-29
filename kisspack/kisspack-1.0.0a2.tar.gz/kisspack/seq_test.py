"""Test group sequences"""


import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_all_tests(params):
    """a list of all tests"""

    test_list = ['test_check_setup']

    test_list.extend(get_normal_tests(params))
    test_list.extend(get_thread_tests(params))
    test_list.extend(get_proc_tests(params))

    return test_list


def get_normal_tests(params):
    """normal mode tests"""

    test_list = ["test_normal_a",
                 "test_normal_b",
                 "test_normal_c",
                 "test_normal_d"]

    return test_list


def get_thread_tests(params):
    """thread mode tests"""

    test_list = ["test_thread_a",
                 "test_thread_b",
                 "test_thread_c",
                 "test_thread_d"]

    return test_list


def get_proc_tests(params):
    """proc mode tests"""

    test_list = ["test_proc_a",
                 "test_proc_b",
                 "test_proc_c",
                 "test_proc_d"]

    return test_list
