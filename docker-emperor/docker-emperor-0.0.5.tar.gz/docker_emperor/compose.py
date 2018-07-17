import six
import os
from docker_emperor.command import Command
from docker_emperor.nodes import HasEnvironment, HasContexts, HasMachines, HasServices, HasVolumes
from docker_emperor.utils import combine, memoized_property, yamp_dump


__all__ = ['Compose']

''' 
Compose stack
Context + Machine
'''

class Compose(HasServices, HasVolumes):


    def __init__(self, root, path="docker-compose"):

        self.root = root
        self.project = self.root.project
        self.machine = self.project.machine
        self.context = self.project.context
        self.name = '{}.{}'.format(self.machine.name, self.context.name)
        self.compose_path = '{}.{}'.format(self.project.name, self.name)
        self.filename = os.path.join(self.root.root_path, 'docker-compose.{}.yml'.format(self.compose_path))
        self.path = "{} -f {}".format(path, self.filename)
 
        self.environment = self.project.environment < self.context.environment < self.machine.environment 
        print(self.environment)
        self.services < self.context.services < self.machine.services 
        for service in self.services:
            service.environment < self.environment
            service['container_name'] = service.get('container_name', '{}.{}.{}'.format(self.project.name, self.name, service.name))
            if not 'image' in service and not 'build' in service:
                service['image'] = service.name
            if 'image' in service:
                if os.path.isfile(os.path.join(self.root.root_path, service['image'], 'Dockerfile')):
                    service['build'] = service['image']
        file = open(self.filename, 'wb')# = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.yml', prefix='docker-compose-', dir=None, delete=False)
        file.write(self.yml)
        file.close()

    @memoized_property
    def data(self): return dict(self.project.data)

    @memoized_property
    def yml(self): 
        self.yml = yamp_dump(self.data)
        for name, value in self.environment:
            self.yml = self.yml.replace('${{{}}}'.format(name), value)
        return self.yml

