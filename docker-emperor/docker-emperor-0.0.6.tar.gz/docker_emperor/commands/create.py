from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    Command(
        root.machine.path, 
        'create', 
        '--driver',
        root.machine.driver,        
        root.machine.name,
        *args,
        is_system=True
    )