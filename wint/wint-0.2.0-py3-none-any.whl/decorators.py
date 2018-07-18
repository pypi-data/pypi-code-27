import functools
import typing

from .container import ContainerProvider
from .descriptor import DependencyDescriptor


def autowired(cls=None, *, container=None):
    container = container or ContainerProvider.get()

    def inner(class_):
        annotations = typing.get_type_hints(cls)

        for attr, typ in annotations.items():
            try:
                getattr(cls, attr)
            except AttributeError:
                setattr(cls, attr, DependencyDescriptor(typ, container))

        return class_

    if cls is not None:
        return inner(cls)

    return functools.partial(autowired, container=container)
