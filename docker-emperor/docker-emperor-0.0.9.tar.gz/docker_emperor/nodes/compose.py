import six
import os
from docker_emperor.commands import Command
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.context import Contexts
from docker_emperor.nodes.machine import Machines
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.volume import Volumes
from docker_emperor.utils import yamp_dump, yaml


__all__ = ['Compose']

''' 
Compose stack Context + Machine 
Combine services & environment vars
'''

class Compose(dict):


    NODES = [
        'services', 
        'volumes', 
        'networks', 
        'version'
    ]

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __repr__(self):
        return '<%s: %s>'.format(self.__class__.__name__, self.name) 

    def __getitem__(self, key): 
        return self.get(key)

    def __init__(self, root, path="docker-compose"):

        self.root = root
        self.project = self.root.project  
        self.machine = self.project.machine
        self.context = self.project.context 
        self.name = '%s.%s.%s' % (self.project.name, self.machine.name, self.context.name)
        self.filename = os.path.join(self.root.root_path, 'docker-compose.%s.yml' % self.name)
        data = dict(self.project)
        for node_name, node in data.items():
            if node_name not in Compose.NODES:
                data.pop(node_name)
        super(Compose, self).__init__(data)
        self['services'] = Services(self['services'])
        self.environment = self.project['environment'].copy()

        self['services'] < self.context['services'] 
        self['services'] < self.machine['services']
        self.environment < self.context['environment'] 
        self.environment < self.machine['environment']
        self.bin = "%s -f %s" % (path, self.filename)
        #self.bin = "%s -f %s --project-directory=%s" % (path, self.filename, self.machine['workdir'])
        # '--project-directory=.',

        for service in self['services']:

            service['environment'] < self.environment
            service['container_name'] = service.get('container_name', '%s.%s' % (self.name, service.name))
            if not 'image' in service and not 'build' in service:
                if os.path.isfile(os.path.join(self.root.root_path, service.name, 'Dockerfile')):
                    service['image'] =  '%s.%s' % (self.project.name, service.name)
                    service['build'] = service.name
                else:
                    service['image'] =  service.name
            else:
                if 'image' in service:
                    if os.path.isfile(os.path.join(self.root.root_path, service['image'], 'Dockerfile')):
                        service['build'] = service['image']

            if not self.machine.is_localhost:
                if 'volumes' in service:

                    new_volumes = []
                    for volume in service['volumes']:
                        print(volume)

                        volume = volume.strip()
                        if volume.startswith('./'):
                            volume = self.machine['workdir'] + volume[2:]
                            new_volumes.append(volume)
                        else:
                            new_volumes.append(volume)
                    service['volumes'] = new_volumes





        file = open(self.filename, 'wb')# = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.yml', prefix='docker-compose-', dir=None, delete=False)
        yml = yamp_dump(self)
        for name, value in self.environment:
            yml = yml.replace('${%s}' % (name), value)
        file.write(yml)
        file.close()

    def copy(self):
        return self.__class__(dict(self))
 
yaml.add_representer(Compose, lambda dumper, data: dumper.represent_dict(data))