import requests

name = 'cutt_sd'
version = '0.0.3'

from .zk import register_api, init, unregister_api, find_api

from .service import register as http_register, unregister as http_unregister, find_api as http_find


def get_myip():
    return requests.get('http://10.9.88.19:5002').text
