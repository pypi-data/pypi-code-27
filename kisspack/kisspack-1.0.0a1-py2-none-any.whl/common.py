"""
Common helper funcs

"""

from distutils.sysconfig import get_python_lib
import logging

import pathlib2 as pathlib
from kissats.schemas.schemas import load_schema

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

PARAM_LOCATION = pathlib.PurePath(get_python_lib(),
                                  "kisspack",
                                  "PARAMS")


def common_task_params():
    """
    Basic params for this package

    """

    yaml_loc = pathlib.PurePath(PARAM_LOCATION, "common_task_params.yaml")
    param_out = load_schema(yaml_loc)

    return param_out
