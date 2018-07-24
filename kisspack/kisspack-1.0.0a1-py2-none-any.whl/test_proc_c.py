"""A test for multiproc mode"""


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
    params['process_safe'] = True
    params['est_task_time'] = (global_params.get('iterations', 10) * 4) + 7
    params['priority'] = 3
    params['req_param_keys'].append("iterations")

    return params


def task_setup(global_params):
    """Setup action for this task."""

    logger.info("execute setup proc c")

    time.sleep(5)

    return


def task_main(global_params):
    """The main task"""

    logger.info("execute task_main proc c")
    result = "Passed"
    task_message = "Nothing to see here"

    avg_delay = 0

    for i in range(0, global_params['iterations']):
        logger.debug("proc_c loop %s", i)
        delay_time = random.random()*3 + 1
        avg_delay = (avg_delay + delay_time)/2

        time.sleep(delay_time)

    global_params["a_new_param"] = "proc c changed me"

    # widget_b_addr should cause this task to throw
    metadata = {"task_message": task_message,
                "avg_delay_time": avg_delay,
                "widget_b_addr": global_params['widget_b_addr'],
                "new_param": global_params.get("a_new_param", "not found")}

    return {'result': result, 'metadata': metadata}


def test_teardown(global_params):
    """Teardown action for this task."""

    logger.info("execute teardown proc c")

    time.sleep(2)
