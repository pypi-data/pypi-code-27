import argparse
import json
import os
from time import sleep

from .get_content import get_content, get_file_content
from .print_results import print_results
from .send_task import send_task
from .server import init


def test(args):
    init()
    parser = argparse.ArgumentParser()
    args = parser.parse_args(args)

    sleep(.5)
    print('Sending requests')

    currentPath = os.getcwd()
    configPath = currentPath + '/cone.json'
    if not os.path.isfile(configPath):
        print('Can not find configuration file <cone.json>')
        return

    data = {
        'objects' : get_content(currentPath),
        'configuration' : json.loads(get_file_content(configPath))
    }

    id = send_task('test', data)
    if id is None:
        print('An error happened: tests have not been sent')
        return

    print_results(id)
