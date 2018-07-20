import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    name = args[0].strip() if args else None
    if name:
        args = list(args)
        args.pop(0)
        machine = root.project['machines'].get(name)
        if machine:
            logger.success(u'Prepare machine <b>%s</b> to be created.' % machine.name)
        else:
            logger.error(u'Machine <b>%s</b> unknow.' % name)
            exit(1)
    else:
        machine = root.machine
        
    if not machine.is_localhost:
        cmd = root.bash(
            machine.bin, 
            'create', 
            '--driver',
            machine['driver'],        
            machine.name,
            *args,
            is_system=True
        )
    else:
        logger.warning(machine.LOCAL_MACHINE_WARNING)