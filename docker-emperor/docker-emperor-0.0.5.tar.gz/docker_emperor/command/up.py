import os
from docker_emperor.command import Command
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
    
    Command(
        root.project.compose.path,
        '--project-directory=.',
        'up',
        env=root.project.machine.docker_env,
        sys=True
    )