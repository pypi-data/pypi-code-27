import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    Command(
        root.project.compose.path,
        'down',
        '--remove-orphans',
        machine=root.project.machine,
        is_system=True
    )