import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):


    # Command(
    #     root.machine.bin,
    #     'mount',
    #     '{}:{}'.format(
    #         root.machine.name, 
    #         os.path.join('/home/docker/', root.compose.project_path)
    #     ),
    #     '.', 
    # )
    root.run_command('machine:start', internal=True)
    root.run_command('hosts:set', internal=True)
    cmd = root.bash(
        root.compose.bin,
        # '--project-directory=.',
        'up',
        machine=root.machine,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is up.' % (root.compose.name, ))

    if root.machine['hosts']:
        for host in root.machine['hosts']:
            logger.success('Project is accessible by http://%s.' % (host, ))

