import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.project.compose.path,
        'logs',
        *args,
        env=root.project.machine.docker_env,
        is_system=True
    )