from docker_emperor.utils import setdefaultdict


__all__ = ['Aliases', 'Aliase']


class Aliases(dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        super(self.__class__, self).__init__(setdefaultdict(data))
        for key, val in self.items(): 
            self[key] = Aliase(key, val)

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        for name, inst in inst.items(): 
            self[name] < inst
        return self

    def __iter__(self):
        for name, inst in self.items(): 
            yield inst

    def __repr__(self):
        return '<{}> \r\n\t - {}'.format(self.__class__.__name__, "\r\n\t - ".join([repr(a) for a in self ]))

    def copy(self):
        return self.__class__(dict(self))


class Aliase(str):

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, args[1])

    def __init__(self, name, data):
        self.name = name
        self.data = data
        super(self.__class__, self).__init__(data)

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        # self.__init__(self.name, combine(inst, self))
        return self

    def __repr__(self):
        return '{}: {}'.format(self.name, self.data)

    def copy(self):
        return self.__class__(self.name, self.data)
