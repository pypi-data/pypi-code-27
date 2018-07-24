"""A test for threading mode"""


import logging
import random
import time

import pathlib2 as pathlib

from kisspack.common import common_task_params


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def get_params(global_params):
    """The parameters for executing the task"""

    params = common_task_params()
    # required keys
    params['name'] = pathlib.Path(__file__).stem
    params['description'] = __doc__
    params['thread_safe'] = True
    params['process_safe'] = False
    params['est_task_time'] = (global_params.get('iterations', 10) * 5) + 5
    params['priority'] = 2
    params['req_param_keys'].append("iterations")
    # test_thread_c should throw so this task should get skipped
    params['prereq_tasks'].append("test_thread_c")

    return params


def task_setup(global_params):
    """Setup action for this task."""

    logger.info("execute setup thread d")

    time.sleep(3)

    return


def task_main(global_params):
    """The main task"""

    logger.info("execute task_main thread d")
    result = "Passed"
    task_message = "Nothing to see here"

    avg_delay = 0

    for i in range(0, global_params['iterations']):
        logger.debug("thread d loop %s", i)
        delay_time = random.random()*3 + 2
        avg_delay = (avg_delay + delay_time)/2

        time.sleep(delay_time)

    metadata = {"task_message": task_message,
                "avg_delay_time": avg_delay,
                "new_param": global_params.get("a_new_param", "not found")}

    return {'result': result, 'metadata': metadata}


def test_teardown(global_params):
    """Teardown action for this task."""

    logger.info("execute teardown thread d")

    time.sleep(2)
