"""Global teardown"""


import logging
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
    params['est_task_time'] = 5
    params['priority'] = 1

    return params


def task_main(global_params):
    """The main task"""

    logger.info("execute task_main global teardown")
    result = "Passed"
    task_message = "Nothing to see here"

    time.sleep(3)

    metadata = {"task_message": task_message,
                "widget_a_sub": global_params.get('widget_a_sub', "not found")}

    return {'result': result, 'metadata': metadata}
