import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    cmd = root.bash(
        root.machine.bin, 
        'create', 
        '--driver',
        root.machine.driver,        
        root.machine.name,
        *args,
        is_system=True
    )