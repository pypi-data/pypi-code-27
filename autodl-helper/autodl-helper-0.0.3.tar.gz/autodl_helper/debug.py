import json
import os


def debug_write_parameter(parameter):
    os.environ['AUTODL_PARAMETER'] = json.dumps(parameter)
