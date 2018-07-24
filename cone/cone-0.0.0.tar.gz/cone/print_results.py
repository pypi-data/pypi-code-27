from time import sleep
import requests

from .error_print import error_print
from .server import get_url

MAX_TRIES = 10

def print_results(id):
    response = requests.get(get_url() + '/results/' + str(id)).json()
    tries = 1
    while response is None and tries < MAX_TRIES:
        response = requests.get(get_url() + '/results/' + str(id)).json()
        sleep(1)
        tries += 1

    if response is not None:
        print(response['out'])
        error_print(response['error_out'])
    else:
        print('Request expired, try again.')
