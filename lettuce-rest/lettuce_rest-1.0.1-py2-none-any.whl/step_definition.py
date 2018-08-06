from lettuce import step, world, before
import sure
import requests
import json
import jpath

SURE_VERSION = sure.version

__all__ = [
    'set_base_url',
    'add_path_to_url',
    'do_not_verify_ssl_certs',
    'verify_ssl_certs',
    'set_header_step',
    'remove_header'
]

WORLD_PREFIX = 'world'


@before.all
def init_lettuce_rest():
    world.headers = {}
    world.base_url = ''
    world.verify_ssl = True


def set_or_resolve(property_name, new_value, special_setter=None):
    """
    This function sets a value for a world property but
    it the value starts with the WORLD_PREFIX then it will
    remove that prefix and try to get the value from the worl
    """
    value_to_set = new_value

    if new_value.startswith(WORLD_PREFIX):
        value_to_set = getattr(world, new_value[len(WORLD_PREFIX) + 1:])

    if special_setter:
        special_setter(value_to_set)
    else:
        setattr(world, property_name, value_to_set)


class SetHeaderHandler:

    def __init__(self, header_name):
        self.header_name = header_name

    def __call__(self, value):
        world.headers[self.header_name] = value


@step('I set base URL to "([^"]*)"')
def set_base_url(step, base_url):
    set_or_resolve('base_url', base_url)


@step('I add path "([^"]*)" to base URL')
def add_path_to_url(step, path):
    world.base_url += "/" + path


@step('I do not want to verify SSL certs')
def do_not_verify_ssl_certs(step):
    world.verify_ssl = False


@step('I want to verify SSL certs')
def verify_ssl_certs(step):
    world.verify_ssl = True


@step('I set "([^"]*)" header to "([^"]*)"')
def set_header_step(step, header_name, header_value):
    header_name = header_name.encode('ascii')
    header_value = header_value.encode('ascii')

    set_header_handler = SetHeaderHandler(header_name)
    set_or_resolve('headers', header_value, set_header_handler)


@step('I clear "([^"]*)" header')
def remove_header(step, header_name):
    world.headers.pop(header_name, None)


@step('I clear all headers')
def remove_all_headers(step):
    world.headers.clear()


@step('I make a "([^"]*)" request to "([^"]*)"')
def request(step, request_verb, url_path_segment):

    url = world.base_url + '/' + url_path_segment

    world.response = \
        getattr(requests, request_verb.lower())(url,
                                                headers=world.headers,
                                                verify=world.verify_ssl)


@step('I make a "([^"]*)" request to "([^"]*)" with parameters')
def request_with_parameters(step, request_verb, url_path_segment):

    url = world.base_url + '/' + url_path_segment

    if len(step.hasesh) is not 1:
        raise Exception('Only one requests is allowed on this sentences')

    params = step.hasesh[0]

    for name, value in params.items():
        params[name] = eval(value) if value.startswith(WORLD_PREFIX) else value

    world.response = \
        getattr(requests, request_verb.lower())(url,
                                                params,
                                                headers=world.headers,
                                                verify=world.verify_ssl)


@step('the response status code should equal "([^"])"')
def status_code_validation(step, expected_http_status_code):
    response = world.response
    str(response.status_code).should.be.equal(expected_http_status_code)


@step('the response status code should not equal "([^"])"')
def status_code_validation_1(step, invalid_http_status_code):
    response = world.response
    str(response.status_code).\
        should.be.different_of(invalid_http_status_code)


@step('the response status code should be among "([^"])"')
def status_code_array_validation(step, expected_http_status_codes):
    response = world.response
    expected_codes_list = \
        [int(x) for x in expected_http_status_codes.split(',')]
    expected_codes_list.should.contain(response.status_code)


@step('the response status message should equal to the following:')
def status_message_validation(step):
    response = world.response
    expected_http_status_message = step.multiline
    response.reason.should_not.be.different_of(expected_http_status_message)


@step('the response status message should looks like to the following:')
def status_message_similarity_validation(step):
    response = world.response
    expected_http_status_message = step.multiline
    response.reason.should.look_like(expected_http_status_message)


@step('the response status message should contains to the following json' +
      'fragment:')
def status_message_json_contains_validation(step):
    response = world.response
    response_json = response.json()

    subset_http_status_message = step.multiline
    subset_http_status_message = subset_http_status_message.encode("utf-8")
    subset_json = json.loads(subset_http_status_message)
    subset_json = dict(map(lambda kv: (helper_unicodo_to_str(kv[0]),
                                       helper_unicodo_to_str(kv[1])),
                           subset_json.iteritems()))

    assert helper_dict_has_dict(response_json, subset_json), \
        "%s can't be found on %s" % (str(subset_json), str(response_json))


@step('the response status message should contains to the following json')
def status_message_json_validation(step):
    response = world.response
    response_json = response.json()

    subset_http_status_message = step.multiline
    subset_http_status_message = subset_http_status_message.encode("utf-8")
    subset_json = json.loads(subset_http_status_message)
    subset_json = dict(map(lambda kv: (helper_unicodo_to_str(kv[0]),
                                       helper_unicodo_to_str(kv[1])),
                           subset_json.iteritems()))

    subset_json.should.equal(response_json)


@step('JSON at path \"(.*)\" should equal(.*)')
def json_object_validation(step, json_path, expected_json_value):
    response = world.response
    data = response.json()
    actual_json_value = jpath.get(json_path, data)

    if expected_json_value.startswith(WORLD_PREFIX):
        expected_json_value = getattr(world,
                                      expected_json_value[len(WORLD_PREFIX):])
    else:
        converted_value = json.loads(expected_json_value)
        actual_json_value.should.be.equal(converted_value)


def helper_unicodo_to_str(msg):
    if isinstance(msg, unicode):
        return msg.encode("utf-8")
    if isinstance(msg, dict):
        return dict(map(lambda kv: (helper_unicodo_to_str(kv[0]),
                                    helper_unicodo_to_str(kv[1])),
                        msg.iteritems()))

    return msg


def helper_dict_has_dict(superset, subset):
    return_value = False

    for superset in superset.values():
        if isinstance(superset, dict):
            return_value |= subset == superset

    return return_value
