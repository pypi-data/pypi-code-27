import six
import collections
from docker_emperor.command import Command
from docker_emperor.nodes import HasEnvironment, HasServices
from docker_emperor.utils import setdefaultdict, combine, memoized_property, memoized, OrderedDict
import docker_emperor.logger as logger


__all__ = ['HasMachines', 'Machines', 'Machine']


# DRIVERS

# Amazon Web Services
# Microsoft Azure
# Digital Ocean
# Exoscale
# Google Compute Engine
# Generic
# Microsoft Hyper-V
# OpenStack
# Rackspace
# IBM Softlayer
# Oracle VirtualBox
# VMware vCloud Air
# VMware Fusion
# VMware vSphere
# VMware Workstation (unofficial plugin, not supported by Docker)
# Grid 5000 (unofficial plugin, not supported by Docker)


class HasMachines():
    
    @memoized_property
    def machines(self):
        attr = '_machines'
        if not hasattr(self, attr): setattr(self, attr, Machines(self.data.pop('machines', dict())))
        return getattr(self, attr)


class Machines():

    DEFAULT = {
        'localhost': {}
    }

    def __init__(self, data):
        self.data = OrderedDict(setdefaultdict(data))
    
    def __repr__(self): 
        return ", ".join(str(m) for m in self)

    def __iter__(self): 
        for name, data in self.data.items():
            yield Machine(name, data)

    def __getitem__(self, i): 
        if isinstance(i, int):
            return [c for c in self][i]
        else:
            if not self.data: 
                return Machine('localhost')
            else:
                return Machine(i, self.data.get(i)) if i in self.data else None


class Machine(HasEnvironment, HasServices):

    COMMANDS = [
        'ssh'
    ]

    class Drivers(object):
        LOCALHOST = 'localhost'
        GENERIC_LOCALHOST = 'generic --generic-ip-address localhost'     

    def __init__(self, name, data={}, path="docker-machine"):

        self.key = name
        self.name = name
        self.data = setdefaultdict(data)
        self.path = path

        # SET DRIVER
        self.driver = self.data.get('driver')
        if not isinstance(self.driver, six.string_types): 
            self.driver = Machine.Drivers.LOCALHOST

        # SET HOSTS
        self.hosts = self.data.get('hosts')
        if not isinstance(self.hosts, list): 
            self.hosts = []

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)



    @property
    def exists(self):
        cmd = self._run("ls", "--filter", "NAME=" + self.name, "--format", "{{.Name}}", env=self.docker_env, tty=False)
        for line in cmd.lines:
            if line == self.name:return True
        return False

    def command_ssh(self, *args, **kwargs):
        self._run('ssh', self.name, *args, **kwargs)

    def command_active(self, *args, **kwargs):
        self._run('active', *args, env=self.docker_env, **kwargs)

    def command_exists(self, *args, **kwargs):
        logger.warning(('Machine {} exists' if self.exists else 'Machine {} doesn\'t exists, execute: dw create').format(self.name))


    @memoized_property
    def docker_env(self):
        if self.driver == Machine.Drivers.LOCALHOST:
            return []
        else:
            cmd = Command(
                self.path, 
                'env', 
                self.name, 
                log=True
            )
            starts = 'export '
            return [line.lstrip(starts) for line in cmd.lines if line.startswith(starts)]

    def start(self):
        if self.driver != Machine.Drivers.LOCALHOST:
            if not self.is_running:
                Command(self.path, 'start', self.name, sys=True).log()  
        return self.is_running


    @property
    def is_running(self):
        return self.status == 'Running'
    
    @property
    def status(self):
        if self.driver == Machine.Drivers.LOCALHOST:
            return 'Running'
        else:
            return Command(self.path, 'status', self.name).out
    
    @property
    def ip(self):
        return Command(self.path, 'ip', self.name, log=False, env=self.docker_env).out.strip()

    @property
    def pwd(self):
        return Command(self.path, 'ssh', self.name, 'pwd', log=False, env=self.docker_env).out.strip()

    @property
    def inspect(self):
        cmd = self._run('inspect', self.name, env=self.docker_env, tty=False)
        return cmd.out

    @property
    def active(self):
        cmd = self._run('active', env=self.docker_env, tty=False)
        return cmd.out

    def remove(self):
        cmd = self._run('rm', self.name, env=self.docker_env)
        return cmd

# active
# config
# create
# env
# help
# inspect
# ip
# kill
# ls
# mount
# provision
# regenerate-certs
# restart
# rm
# scp
# ssh
# start
# stop
# upgrade
# url

Command.Machine = Machine