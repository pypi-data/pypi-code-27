import os
from docker_emperor.command import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    Command(
        root.project.compose.path,
        'logs',
        *args,
        env=root.project.machine.docker_env,
        sys=True
    )