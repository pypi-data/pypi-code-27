"""
Teardown sequences

"""

import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_global_teardown(params):
    """Global teardown"""

    teardown_list = ['teardown_global']

    return teardown_list


def get_thread_teardown(params):
    """teardown steps for thread"""

    teardown_list = ["teardown_clear_param"]

    return teardown_list
