from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    m = root.project.machine
    
    if m.is_localhost:
        logger.warning('You are already on a local machine')
    else:
        cmd = root.bash(
            m.path, 
            'ssh', 
            m.name,
            *args,
            is_system=True
        )
        if cmd.is_success:
            logger.success('You are already on a local machine')
