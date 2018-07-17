import os
import six
from docker_emperor.nodes import HasEnvironment, HasContexts, HasMachines, HasServices, HasAliases
from docker_emperor.compose import Compose
from docker_emperor.exceptions import DockerEmperorException
from docker_emperor.utils import setdefaultdict, memoized_property, combine, yamp_load
import docker_emperor.logger as logger


class Project(HasEnvironment, HasContexts, HasMachines):

    def __init__(self, root):

        self.root = root
        self.config = setdefaultdict(root.projects, self.name, {})
        self.config['workdir'] = os.path.abspath(self.root.root_path)

    FILES = ['docker-emperor.yml', 'docker-compose.yml']
    @memoized_property
    def data(self):
        for file in self.FILES:
            filename = os.path.join(self.root.root_path, file)
            if os.path.isfile(filename):
                data = yamp_load(open(filename, 'rb').read())
                if not isinstance(data, dict):
                    raise DockerEmperorException('{} is not yml as dict'.format(os.path.basename(file)))
                return data
        raise DockerEmperorException('{} not found in {}'.format(" or ".join(self.FILES), self.root.root_path))

    @memoized_property
    def name(self): 
        return self.data.pop('name',  
            self.data.pop('project_name',                       # default 0
                self.environment.get('COMPOSE_PROJECT_NAME',    # default 1
                    os.environ.get('COMPOSE_PROJECT_NAME',      # default 2
                        os.path.basename(self.root.root_path)   # default 3
                    )
                )
            )
        )

    def run_aliase_command(self, name, *args):
        aliases = self.aliases < self.context.aliases < self.machine.aliases 


    @memoized_property
    def compose(self): 
        return Compose(self.root)

    @property
    def context(self):
        if not hasattr(self, '__context'):
            context = self.contexts[self.config.get('context')]
            if not context:
                self.ask_context()
                return self.context
            else:
                setattr(self, '__context', context)
        return getattr(self, '__context')

    @property
    def machine(self):  
        if not hasattr(self, '__machine'):      
            machine = self.machines[self.config.get('machine')]
            if not machine:
                self.root.run_command('machine:set')
                return self.machine
            else:
                setattr(self, '__machine', machine)
        return getattr(self, '__machine')

