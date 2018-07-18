import pickle

from caller.base_types import base_types


def call(obj, *args, **kwargs):
    return obj.__call__(*args, **kwargs)


def make_callable(value, func, cache={}):
    try:
        value_type = value.__class__
    except AttributeError:
        value_type = type(value)
    cls_name = "Callable{cls}".format(cls=value_type.__name__.capitalize())
    bases = (base_types.get(value_type, value_type),)
    attributes = {
        "__call__": call,
        "__class__": value_type,
        "__iadd__": lambda _, other: value + other,
    }
    if cls_name not in cache:
        callable_type = type(cls_name, bases, attributes)
        try:
            reduce = pickle.Pickler.dispatch[value_type]
            pickle.Pickler.dispatch[callable_type] = reduce
        except (AttributeError, KeyError):
            pass
        cache[cls_name] = callable_type
    else:
        callable_type = cache[cls_name]
    callable_value = callable_type(value)
    callable_value.__call__ = func
    for attr_name in dir(value):
        try:
            if attr_name not in attributes:
                setattr(callable_value, attr_name, getattr(value, attr_name))
        except AttributeError:
            pass
    return callable_value
