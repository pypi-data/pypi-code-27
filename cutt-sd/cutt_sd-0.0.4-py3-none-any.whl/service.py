import requests

from cutt_sd.config import *


def register(uri, port, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'register',
        'port': port,
        'uri': uri,
        'env': env
    })


def unregister(uri, port, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'unregister',
        'port': port,
        'uri': uri,
        'env': env
    })


def find_api(uri, env=DEFAULT_ENV, sd_server=DEFAULT_SERVER):
    response = requests.post(sd_server + 'query', {'uri': uri, 'env': env})
    return response.text
