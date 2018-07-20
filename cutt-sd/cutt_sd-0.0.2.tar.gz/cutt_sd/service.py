import os

import requests

DEFAULT_SERVER = os.environ['SD_SERVER'] if 'SD_SERVER' in os.environ else 'http://localhost:4367/'


def register(uri, port, env='cutt', sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'register',
        'port': port,
        'uri': uri,
        'env': env
    })


def unregister(uri, port, env='cutt', sd_server=DEFAULT_SERVER):
    requests.post(sd_server, {
        'action': 'unregister',
        'port': port,
        'uri': uri,
        'env': env
    })


def find_api(uri, env='cutt', sd_server='http://localhost:4367/'):
    response = requests.post(sd_server + 'query', {'uri': uri, 'env': env})
    return response.text
