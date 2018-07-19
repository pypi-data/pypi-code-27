import os
import six
import collections
from docker_emperor.commands import Command
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.aliase import Aliases
from docker_emperor.utils import setdefaultdict, OrderedDict
import docker_emperor.logger as logger


__all__ = ['Machines', 'Machine']


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


class Machines(dict):

    DEFAULT = {
        'localhost': {}
    }

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        super(self.__class__, self).__init__(setdefaultdict(data))
        if self:
            for key, val in self.items():
                self[key] = Machine(key, val)
        else:
            self['localhost'] = Machine('localhost')
    
    def __iter__(self):
        for key, val in self.items():
            yield val
            
    def __repr__(self): 
        return ", ".join(str(m) for m in self)

    def __getitem__(self, i): 
        if isinstance(i, int):
            return [c for c in self][i]
        else:
            return self.get(i, None)


class Machine(dict):

    COMMANDS = [
        'ssh'
    ]

    class Drivers(object):
        LOCALHOST = 'localhost'
        GENERIC_LOCALHOST = 'generic --generic-ip-address localhost'  

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)   

    def __init__(self, name, data={}, bin="docker-machine"):
        self.key = name
        self.name = name
        self.bin = bin
        super(Machine, self).__init__(setdefaultdict(data))
        for default_name, default_class in [
            ('environment', Environment),
            ('services', Services),
            ('aliases', Aliases),
        ]:
            self[default_name] = default_class(self[default_name])
        # SET DRIVER
        if not isinstance(self['driver'], six.string_types): 
            self['driver'] = Machine.Drivers.LOCALHOST
        # SET HOSTS
        if not isinstance(self['hosts'], list): 
            self['hosts'] = []


    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def __getitem__(self, key): 
        return self.get(key)

    @property
    def is_localhost(self):
        return self['driver'] == Machine.Drivers.LOCALHOST

    @property
    def exists(self):
        cmd = self._run("ls", "--filter", "NAME=" + self.name, "--format", "{{.Name}}", env=self.docker_env, tty=False)
        for line in cmd.lines:
            if line == self.name:return True
        return False

    @property
    def docker_env(self):
        n = '__docker_env'
        if not hasattr(self, n):
            if self.is_localhost:
                env = []
            else:
                cmd = Command(
                    self.path, 
                    'env', 
                    self.name, 
                    log=True
                )
                starts = 'export '
                env = [line.lstrip(starts) for line in cmd.lines if line.startswith(starts)]
            setattr(self, n, env)
        return getattr(self, n)

    def start(self):
        if self.is_localhost:
            if not self.is_running:
                Command(self.path, 'start', self.name, sys=True).run().log()  
        return self.is_running

    @property
    def is_running(self):
        return self.status == 'Running'
    
    @property
    def status(self):
        if self.is_localhost:
            return 'Running'
        else:
            return Command(self.path, 'status', self.name).run().out
    
    @property
    def ip(self):
        if self.is_localhost:
            return '0.0.0.0'
        else:
            return Command(self.path, 'ip', self.name, log=False, env=self.docker_env).run().out.strip()

    @property
    def pwd(self):
        return Command(self.path, 'ssh', self.name, 'pwd', log=False, env=self.docker_env).run().out.strip()

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