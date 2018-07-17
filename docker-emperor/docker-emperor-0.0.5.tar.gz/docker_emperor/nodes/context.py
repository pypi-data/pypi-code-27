import six
from docker_emperor.nodes import HasEnvironment, HasServices
from docker_emperor.utils import setdefaultdict, combine, memoized_property, memoized, OrderedDict


__all__ = ['HasContexts', 'Contexts', 'Context']


class HasContexts():
    
    @property
    def contexts(self):
        attr = '_contexts'
        if not hasattr(self, attr): 
            setattr(self, attr, Contexts(self.data.pop('contexts', {})))
        return getattr(self, attr)


class Contexts():

    def __init__(self, data):
        self.data = OrderedDict(setdefaultdict(data))

    def __repr__(self): 
        return ", ".join(str(c) for c in self)

    def __iter__(self): 
        for name, data in self.data.items():
            yield Context(name, data)

    def __getitem__(self, i): 
        if not self.data:
            return []
        if isinstance(i, int):
            return [c for c in self][i]
        else:
            if not self.data: 
                return Context('default')
            else:
                return Context(i, self.data.get(i)) if i in self.data else None




class Context(HasEnvironment, HasServices):

    COMMANDS = [
    ]


    def __init__(self, name, data={}):

        self.name = name
        self.data = setdefaultdict(data)

    @classmethod
    def has_command(cls, name):
        return hasattr(cls, 'command_{}'.format(name))

    def run_command(self, name, *args):
        if Context.has_command(name):
            getattr(self, 'command_{}'.format(name))(*args)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


    # def combine_services(self):

    #     for name, service in self.data.get('services', {}).items():
    #         if service:
    #             service['environment'] = combine(service.get('environment'), self.environment, as_varlist=True)
    #             service['container_name'] = service.get('container_name', '{}.{}.{}'.format(self.project_name, self.name, name))
    #             if not 'image' in service and not 'build' in service:
    #                 service['image'] = name
    #             if 'image' in service:
    #                 if os.path.isdir(service['image']):
    #                     service['build'] = service['image']

    # @property
    # def compose_filename(self):

    #     if not hasattr(self, '_yml'):

    #         self.data.pop('shortcuts', {})

    #         self.yml = yaml.dump(self.data, Dumper=YamlDumper, default_flow_style=False, indent=4)
    #         for name, value in varlist_to_dict(self.environment).items():
    #             self.yml = self.yml.replace('${{{}}}'.format(name), value)

    #         self.compose_filename = os.path.join(self.root.root, 'docker-compose.{}.{}.yml'.format(self.project_name, self.name))
    #         self.compose_file = open(self.compose_filename, 'wb')# = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.yml', prefix='docker-compose-', dir=None, delete=False)
    #         self.compose_file.write(self.yml)
    #         self.compose_file.close()

    #         setattr(self, '_yml')

    #     return getattr(self, '_yml')
