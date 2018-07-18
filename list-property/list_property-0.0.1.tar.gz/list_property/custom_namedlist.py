from .custom_property import list_property


__all__ = ['NamedList', 'namedlist']


class NamedListMetaclass(type):
    def __new__(typ, name, bases, attrs):
        cls = super().__new__(typ, name, bases, attrs)
        cls.__properties__ = [attr for attr in dir(cls) if isinstance(getattr(cls, attr), list_property)]
        return cls


class NamedList(list, metaclass=NamedListMetaclass):
    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            args = [args]
        super().__init__(*args)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __iter__(self):
        self.__current_index__ = 0
        return self

    def __next__(self):
        idx = self.__current_index__
        self.__current_index__ += 1
        try:
            return self[idx]
        except:
            raise StopIteration

    def __getitem__(self, i):
        try:
            return super().__getitem__(i)
        except IndexError as err:
            try:
                attr = self.__properties__[i]
                prop = getattr(self.__class__, attr)
                return prop.fget(self)
            except:
                pass
            raise err

    # def __str__(self):
    #     return '[{0}]'.format(', '.join((repr(i) for i in self)))


def _get_value(obj, index, default=None):
    try:
        return obj[index]
    except:
        return default


def namedlist(name, field_names, defaults=None):
    if not isinstance(field_names, (list, tuple)):
        field_names = field_names.split()

    if isinstance(defaults, dict):
        fields = {name: list_property(i, defaults.get(name, None)) for i, name in enumerate(field_names)}
    elif isinstance(defaults, (list, tuple)):
        fields = {name: list_property(i, _get_value(defaults, i, None)) for i, name in enumerate(field_names)}
    else:
        fields = {name: list_property(i, defaults) for i, name in enumerate(field_names)}

    return type(name, (NamedList,), fields)
