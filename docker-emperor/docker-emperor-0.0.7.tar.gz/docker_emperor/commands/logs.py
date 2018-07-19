import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.bin,
        'logs',
        *args,
        machine=root.project.machine,
        is_system=True
    )