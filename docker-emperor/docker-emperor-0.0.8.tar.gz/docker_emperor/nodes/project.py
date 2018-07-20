import os
import six
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.machine import Machines
from docker_emperor.nodes.context import Contexts
from docker_emperor.nodes.aliase import Aliases
from docker_emperor.nodes.compose import Compose 
from docker_emperor.commands import Command 
from docker_emperor.exceptions import DockerEmperorException
from docker_emperor.utils import setdefaultdict,  yamp_load
import docker_emperor.logger as logger


__all__ = ['Project']


class Project(dict):

    FILES = ['docker-emperor.yml', 'docker-compose.yml']

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def __getitem__(self, key): 
        return self.get(key)

    def __init__(self, root):
        self.root = root
        super(Project, self).__init__(self.get_yml_data())
        for default_name, default_class in [
            ('environment', Environment),
            ('contexts', Contexts),
            ('machines', Machines),
            ('aliases', Aliases),
        ]:
            self[default_name] = default_class(self[default_name])        
        self.config = setdefaultdict(root.projects, self.name, {})
        self.config['workdir'] = os.path.abspath(self.root.root_path)

    def get_yml_data(self):
        for file in self.FILES:
            filename = os.path.join(self.root.root_path, file)
            if os.path.isfile(filename):
                data = yamp_load(open(filename, 'rb').read())
                if not isinstance(data, dict):
                    raise DockerEmperorException('{} is not yml as dict'.format(os.path.basename(file)))
                return data
        raise DockerEmperorException('{} not found in {}'.format(" or ".join(self.FILES), self.root.root_path))

    @property
    def name(self): 
        n = '__name'
        if not hasattr(self, n):
            setattr(self, n, self.pop('name',  
                self.pop('project_name',                       # default 0
                    self['environment'].get('COMPOSE_PROJECT_NAME',    # default 1
                        os.environ.get('COMPOSE_PROJECT_NAME',      # default 2
                            os.path.basename(self.root.root_path)   # default 3
                        )
                    )
                )
            ))
        return getattr(self, n)

    def run_aliase_command(self, name, *args):
        aliases = self['aliases']
        aliases < self.context['aliases'] 
        aliases < self.machine['aliases']
        if name in aliases:
            aliase = aliases[name]
            for command in aliase.commands:
                if command == name:
                    logger.error('Comand loop error: <b>%s</b>' % (command))
                else:
                    logger.cmd('Run custom aliase <b>%s</b> : %s %s' % (aliase.name, command, " ".join(args)))
                    cmd = self.root.bash(
                        'docker-emperor',
                        command,
                        *args,
                        machine=self.machine,
                        is_system=True
                    )
            return True
        return False


    @property
    def compose(self): 
        n = '__compose'
        if not hasattr(self, n):
            setattr(self, n, Compose(self.root))
        return getattr(self, n)

    @property
    def context(self):
        n = '__context'
        if not hasattr(self, n):
            context = self['contexts'][self.config.get('context')]
            if not context:
                self.root.run_command('context:set', internal=True)
                return self.context
            else:
                setattr(self, n, context)
        return getattr(self, n)

    @property
    def machine(self): 
        n = '__machine' 
        if not hasattr(self, n):
            machine = self['machines'][self.config.get('machine')]
            if not machine:
                self.root.run_command('machine:set', internal=True)
                return self.machine
            else:
                setattr(self, n, machine)
        return getattr(self, n)