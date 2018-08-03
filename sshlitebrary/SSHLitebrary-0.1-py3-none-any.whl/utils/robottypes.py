from collections import Mapping, UserString
from io import IOBase


def is_integer(item):
    return isinstance(item, int)


def is_number(item):
    return isinstance(item, (int, float))


def is_bytes(item):
    return isinstance(item, (bytes, bytearray))


def is_string(item):
    return isinstance(item, str)


def is_unicode(item):
    return isinstance(item, str)


def is_list_like(item):
    if isinstance(item, (str, bytes, bytearray, UserString, IOBase)):
        return False
    try:
        iter(item)
    except (KeyboardInterrupt, SystemExit, MemoryError):
        raise
    except:
        return False
    else:
        return True


def is_dict_like(item):
    return isinstance(item, Mapping)


def type_name(item):
    if isinstance(item, IOBase):
        return 'file'
    cls = item.__class__ if hasattr(item, '__class__') else type(item)
    named_types = {str: 'string', bool: 'boolean', int: 'integer',
                   type(None): 'None', dict: 'dictionary', type: 'class'}
    return named_types.get(cls, cls.__name__)

def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '')
    return bool(item)


def is_falsy(item):
    return not is_truthy(item)
