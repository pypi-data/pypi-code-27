import os
from docker_emperor.nodes import HasEnvironment, HasVolumes
from docker_emperor.utils import combine, memoized_property, yaml


__all__ = ['HasAliases', 'Aliases', 'Aliase']


class HasAliases():

    @memoized_property
    def aliases(self):
        attr = '_aliases'
        if not hasattr(self, attr): setattr(self, attr, Aliases(self.data.pop('aliases', dict())))
        return getattr(self, attr)


class Aliases(dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        if not isinstance(data, dict): data = {}
        super(Aliases, self).__init__(data)
        for name, data in self.items(): self[name] = Aliase(name, data)

    def __gt__(self, aliases):
        if not isinstance(aliases, Aliases): return self
        return aliases < self

    def __lt__(self, aliases):
        if not isinstance(aliases, Aliases): return self
        for aliase in aliases:
            aliase < self.get(aliase.name)
        return self

    def __iter__(self):
        for name, aliase in self.items():
            yield aliase

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, super(dict, self).__repr__())

    @property
    def data(self): return self

def aliases_representer(dumper, aliases):
    return dumper.represent_dict(aliases)
yaml.add_representer(Aliases, aliases_representer)


class Aliase(dict):

    preserve_environment = True

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, name, data):
        self.name = name
        if not isinstance(data, dict): data = {}
        super(Aliase, self).__init__(data)

    def __gt__(self, aliase):
        if not isinstance(aliase, Aliase): return self
        return aliase < self

    def __lt__(self, aliase):
        if not isinstance(aliase, Aliase): return self
        self.__init__(self.name, combine(aliase, self))
        return self

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    @property
    def data(self): return self
    

def aliase_representer(dumper, aliase):
    return dumper.represent_dict(aliase)
yaml.add_representer(Aliase, aliase_representer)
