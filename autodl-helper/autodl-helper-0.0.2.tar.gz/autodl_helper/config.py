# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import sys
import json
import os
import requests
import six

session = requests.Session()


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        super(DotDict, self).__init__()
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value

    def __delitem__(self, key):
        super(DotDict, self).__delitem__(key)
        del self.__dict__[key]

    # setstate and getstate is for pickle
    def __getstate__(self):
        pass

    def __setstate__(self, *args, **kwargs):
        pass


def _load_json(str):
    if sys.version_info.major >= 3:
        return json.loads(str)

    def json_loads_byteified(json_text):
        return _byteify(
            json.loads(json_text, object_hook=_byteify),
            ignore_dicts=True
        )

    def _byteify(data, ignore_dicts=False):
        if isinstance(data, unicode):
            return data.encode('utf-8')
        if isinstance(data, list):
            return [_byteify(item, ignore_dicts=True) for item in data]
        if isinstance(data, dict) and not ignore_dicts:
            return {
                _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
            }
        return data

    return json_loads_byteified(str)


_parameter = None


def get_parameter():
    global _parameter
    if _parameter is not None:
        return _parameter
    parameter = os.getenv('AUTOCNN_PARAMETER', None)
    try:
        param = DotDict(_load_json(parameter)) if parameter else None
        _parameter = param
        return _parameter
    except Exception as e:
        print('Could get parameters. {}'.format(e))
        return None


def write_parameter():
    argv = sys.argv
    if argv[1] == 'write' and len(argv) > 2:
        output_yml = argv[2]
    else:
        print('Write Failed !!!\nUsage `helper write yml_file_name` to write parameters to yml')
        sys.exit(1)
    parameter = os.getenv('AUTOCNN_PARAMETER', None)
    try:
        if parameter is None:
            raise ValueError('Parameter is None')
        path = os.path.dirname(output_yml)
        if path and not os.path.isdir(path):
            os.makedirs(path)
        with open(output_yml, 'w') as fo:
            fo.write(parameter)
    except Exception as e:
        print('Could get parameters. {}'.format(e))


def get_exp_info():
    """Returns :
        * project_name
        * exp_name
        * project_uuid
        * exp_uuid
    """
    info = os.getenv('AUTOCNN_TASK_INFO', None)
    try:
        return json.loads(info) if info else None
    except (ValueError, TypeError):
        print('Could get exp info, '
              'please make sure this is running inside a autodl job.')
        return None


def get_api(version='v1'):
    api = os.getenv('AUTOCNN_API', None)
    if not api:
        print('Could get api info, '
              'please make sure this is running inside a autodl job.')
        return None
    return '{}/api/{}'.format(api, version)


def get_user_token():
    return os.getenv('AUTOCNN_USER_TOKEN', None)


def send_metrics(**metrics):
    exp_info = get_exp_info()
    exp_name = exp_info.get('exp_name', None)
    user_token = get_user_token()
    api = get_api()
    if not all([exp_name, user_token, api]):
        print('Environment information not found, '
              'please make sure this is running inside a autodl job.')
        return

    values = exp_name.split('.')
    user, project, exp = values[0], values[1], values[-1]

    try:
        formatted_metrics = {k: float(v) for k, v in six.iteritems(metrics)}
    except (ValueError, TypeError):
        print('Could not send metrics {}'.format(metrics))
        return

    try:
        session.post('{}/exp/{}/{}/{}/metrics/'.format(api, user, project, exp),
                     headers={"Authorization": "token {}".format(user_token)},
                     data={'values': json.dumps(formatted_metrics)},
                     timeout=0.1)
    except requests.RequestException as e:
        print('Could not reach autodl api {}'.format(e))
