"""setup a new param in the global params"""


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
    params['est_task_time'] = 6
    params['priority'] = 7

    return params


def task_main(global_params):
    """The main task"""

    logger.info("execute task_main setup set_param")
    result = "Passed"
    task_message = "Nothing to see here"

    delay_time = random.random()*5 + 1

    time.sleep(delay_time)

    global_params["a_new_param"] = "set by setup_set_param"

    metadata = {"task_message": task_message}

    return {'result': result, 'metadata': metadata}
