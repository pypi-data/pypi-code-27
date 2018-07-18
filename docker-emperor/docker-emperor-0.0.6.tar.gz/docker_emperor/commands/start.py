import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    root.project.machine.start()
    root.run_command('down')
    root.run_command('up')