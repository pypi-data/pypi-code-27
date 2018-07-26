
import subprocess
import json
import xmltodict
from functools import wraps
from flask import make_response, jsonify
from clusterAPI import api


def xml_to_json(xml_data):
    return json.dumps(xmltodict.parse(xml_data))


def to_ascii(s):
    '''
    Convert the bytes string to a ASCII string
    Usefull to remove accent (diacritics)
 
    From crmsh.utils
    '''
    if s is None:
        return s
    if isinstance(s, str):
        return s
    try:
        return str(s, 'utf-8')
    except UnicodeDecodeError:
        import traceback
        traceback.print_exc()
        return s


def get_stdout_stderr(cmd, input_s=None, shell=True):
    '''
    Run a cmd, return (rc, stdout, stderr)

    From crmsh.utils
    '''
    proc = subprocess.Popen(cmd,
                            shell=shell,
                            stdin=input_s and subprocess.PIPE or None,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout_data, stderr_data = proc.communicate(input_s)
    return proc.returncode, to_ascii(stdout_data), to_ascii(stderr_data)


def get_cib_data_raw(scope=None):
    get_cib_cmd = "%s %s" % \
                  (api.config['CIB_CMD'], api.config['CIB_CMD_OPTIONS'])
    if scope:
        get_cib_cmd += " -o %s" % scope
    ret, out, err = get_stdout_stderr(get_cib_cmd)
    return out


def get_cib_data(scope=None):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            g['cib_data'] = xml_to_json(get_cib_data_raw(scope))  
            return f(*args, **kwargs)

        g = f.__globals__
        return decorator_function
    return decorator


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code


def response_auth(status, message, token, status_code):
    """
    Make a Http response to send the auth token
    :param status: Status
    :param message: Message
    :param token: Authorization Token
    :param status_code: Http status code
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': status,
        'message': message,
        'auth_token': token.decode("utf-8")
    })), status_code
