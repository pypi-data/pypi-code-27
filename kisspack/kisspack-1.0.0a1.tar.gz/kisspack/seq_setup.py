"""
Setup sequences

"""

import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_global_setup(params):
    """Global setup"""

    setup_list = ["setup_set_param"]

    return setup_list


def get_all_setup(params):
    """a list of all setup tasks"""

    setup_list = ['test_check_setup']

    setup_list.extend(get_normal_setup(params))
    setup_list.extend(get_thread_setup(params))
    setup_list.extend(get_proc_setup(params))

    return setup_list


def get_normal_setup(params):
    """normal mode setup"""

    setup_list = []

    return setup_list


def get_thread_setup(params):
    """thread mode setup"""

    setup_list = []

    return setup_list


def get_proc_setup(params):
    """proc mode setup"""

    setup_list = ["setup_proc"]

    return setup_list
