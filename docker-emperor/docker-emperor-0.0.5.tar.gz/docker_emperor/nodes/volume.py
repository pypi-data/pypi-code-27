import os
from docker_emperor.utils import combine, memoized_property, yaml


__all__ = ['HasVolumes', 'Volumes', 'Volume']


class HasVolumes():

    preserve_volumes = True

    @memoized_property
    def volumes(self):
        if self.preserve_volumes:
            self.data['volumes'] = Volumes(self.data.get('volumes', list()))
            return self.data['volumes']
        else:
            return Volumes(self.data.pop('volumes', list()))


class Volumes():

    def __init__(self, data):
        if not isinstance(data, dict): data = {}
        super(Volumes, self).__init__(data)
        for name, data in self.items(): self[name] = Volume(name, data)

    def __gt__(self, volumes):
        if not isinstance(volumes, Volumes): return self
        return volumes < self

    def __lt__(self, volumes):
        if not isinstance(volumes, Volumes): return self
        for volume in volumes:
            volume < self.get(volume.name)
        return self

    def __iter__(self):
        for name, volume in self.items():
            yield volume

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, super(dict, self).__repr__())

    @property
    def data(self): return self

def volumes_representer(dumper, volumes):
    return dumper.represent_dict(volumes)
yaml.add_representer(Volumes, volumes_representer)


class Volume():

    preserve_environment = True

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, name, data):
        self.name = name
        if not isinstance(data, dict): data = {}
        super(Volume, self).__init__(data)

    def __gt__(self, volume):
        if not isinstance(volume, Volume): return self
        return volume < self

    def __lt__(self, volume):
        if not isinstance(volume, Volume): return self
        self.__init__(self.name, combine(volume, self))
        return self

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    @property
    def data(self): return self
    

def volume_representer(dumper, volume):
    return dumper.represent_dict(volume)
yaml.add_representer(Volume, volume_representer)