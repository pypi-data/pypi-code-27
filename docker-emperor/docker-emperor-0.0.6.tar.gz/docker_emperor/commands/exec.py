import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    root.project.machine.start()
    root.bash(
        root.project.compose.path,
        'exec', 
        *args,
        machine=root.project.machine,
        is_system=True
    )