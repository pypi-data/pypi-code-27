"""A test to test prereq order"""


import logging
import random
import time

import pathlib2 as pathlib

from kisspack.common import common_task_params


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_params(global_params):
    """
    The parameters for executing the task

    """

    params = common_task_params()
    # required keys
    params['name'] = pathlib.Path(__file__).stem
    params['description'] = __doc__
    params['est_task_time'] = 8
    params['priority'] = 1
    params['prereq_tasks'] = list()

    return params


def task_setup(global_params):
    """Setup action for this task."""

    logger.info("execute setup check setup")

    time.sleep(2)

    return


def task_main(global_params):
    """The main task"""

    logger.info("execute task_main setup check")
    result = "Passed"
    task_message = "Nothing to see here"

    delay_time = random.random()*2 + 1
    time.sleep(delay_time)

    metadata = {"task_message": task_message,
                "widget_a_sub": global_params.get('widget_a_sub', "not found"),
                "new_param": global_params.get("a_new_param", "not found")}

    return {'result': result, 'metadata': metadata}


def test_teardown(global_params):
    """Teardown action for this task."""

    logger.info("execute teardown setup check")

    time.sleep(3)
