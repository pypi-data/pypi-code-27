from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    machine = root.machine
    
    if machine.is_localhost:
        logger.warning(machine.LOCAL_MACHINE_WARNING)
    else:
        cmd = root.bash(
            machine.bin, 
            'ssh', 
            machine.name,
            *args,
            is_system=True
        )
        if cmd.is_success:
            logger.success('')
