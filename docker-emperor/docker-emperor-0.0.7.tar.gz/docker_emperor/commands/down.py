import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    Command(
        root.compose.bin,
        'down',
        '--remove-orphans',
        machine=root.machine,
        is_system=True
    )