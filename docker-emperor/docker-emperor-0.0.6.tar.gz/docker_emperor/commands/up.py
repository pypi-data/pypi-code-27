import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):


    # Command(
    #     root.machine.path,
    #     'mount',
    #     '{}:{}'.format(
    #         root.machine.name, 
    #         os.path.join('/home/docker/', root.compose.project_path)
    #     ),
    #     '.', 
    # )
    
    cmd = root.bash(
        root.project.compose.path,
        # '--project-directory=.',
        'up',
        machine=root.project.machine,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is up.' % (root.project.compose.compose_path, ))
