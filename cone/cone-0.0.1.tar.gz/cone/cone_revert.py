import argparse
from time import sleep

from .print_results import print_results
from .send_task import send_task
from .server import init


def revert(args):
    init()
    parser = argparse.ArgumentParser()
    args = parser.parse_args(args)

    sleep(.5)

    id = send_task('revert', {})
    if id is None:
        print('An error happened: tests have not been sent')
        return

    print_results(id)
