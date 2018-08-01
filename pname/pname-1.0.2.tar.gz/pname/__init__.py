import requests
import json
from colorama import Fore, Style, init
init()

def check(pname):
    endpoint = 'https://pypi.org/pypi/' + pname + '/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        print(Fore.RED + '✘ ' + Style.RESET_ALL + pname + ' is unavailable')
    else:
        print(Fore.GREEN + '✔ ' + Style.RESET_ALL + pname + ' is available')
