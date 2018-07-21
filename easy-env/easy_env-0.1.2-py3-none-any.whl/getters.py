import base64
import os
from typing import Callable, Optional, Type, TypeVar, Union, overload


__all__ = [
    'get_int', 'get_float', 'get_bool', 'get_str', 'get_bytes', 'get_list', 'get',
]
TRUE_VALUES = set('1 true t yes y ok okay confirm absolutely totally yep'.split())
FALSE_VALUES = set("0 false f no n bad nope don't".split())
T = TypeVar('T')


@overload
def process(key: str, default: None = None,
            factory: Union[Callable[[str], T], Type[T]] = str,
            raise_error: bool = False) -> Optional[T]: ...


@overload
def process(key: str, default: T = None,
            factory: Union[Callable[[str], T], Type[T]] = str,
            raise_error: bool = False) -> T: ...


def process(key, default=None, factory=str, raise_error=False):
    value = os.getenv(key, None)
    if value is None:
        if default is not None:
            value = default
        elif raise_error:
            raise KeyError('Failed to find env var {}'.format(key))
    else:
        value = factory(value)
    return value


def bool_factory(value: str) -> bool:
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    raise ValueError("Bad boolean value.")


def list_factory(value: str, separator: str, item_factory):
    return list(map(item_factory, value.split(separator)))


# GET INT

@overload
def get_int(key: str, default: None = None, raise_error=False, **_) -> Optional[int]: ...


@overload
def get_int(key: str, default: int, raise_error=False, **_) -> int: ...


def get_int(key, default=None, raise_error=False, **_):
    return process(key, default, int, raise_error)


# GET FLOAT

@overload
def get_float(key: str, default: None = None, raise_error=False, **_) -> Optional[float]: ...


@overload
def get_float(key: str, default: float, raise_error=False, **_) -> float: ...


def get_float(key, default=None, raise_error=False, **_):
    return process(key, default, float, raise_error)


# GET STR

@overload
def get_str(key: str, default: None = None, raise_error=False, **_) -> Optional[str]: ...


@overload
def get_str(key: str, default: str, raise_error=False, **_) -> str: ...


def get_str(key, default=None, raise_error=False, **_) -> Optional[str]:
    return process(key, default, lambda x: str(x), raise_error)


# GET BOOL

@overload
def get_bool(key: str, default: None = None, raise_error=False, **_) -> Optional[bool]: ...


@overload
def get_bool(key: str, default: bool, raise_error=False, **_) -> bool: ...


def get_bool(key, default=None, raise_error=False, **_):
    return process(key, default, bool_factory, raise_error)


# GET BYTES

@overload
def get_bytes(key: str, default: None = None, raise_error=False, **_) -> Optional[bytes]: ...


@overload
def get_bytes(key: str, default: bytes, raise_error=False, **_) -> bytes: ...


def get_bytes(key, default=None, raise_error=False, **_):
    return process(key, default, base64.b64decode, raise_error)


# GET LIST

@overload
def get_list(key: str, default: None = None, raise_error=False, **_) -> Optional[list]: ...


@overload
def get_list(key: str, default: list, raise_error=False, **_) -> list: ...


def get_list(key, default=None, raise_error=False, **kwargs):
    separator = kwargs.pop('separator', ',')
    item_factory = kwargs.pop('item_factory', str)
    return process(key, default,
                   lambda x: list_factory(x, separator, item_factory),
                   raise_error)


def based_on_default(key: str, default: Optional[int] = None,
                     raise_error=False, **kwargs):
    type_mapper = {
        int: get_int,
        float: get_float,
        str: get_str,
        bool: get_bool,
        bytes: get_bytes,
        list: get_list,
    }
    default_type = type(default)
    if default_type in type_mapper:
        getter = type_mapper[default_type]
        return getter(key, default, raise_error, **kwargs)
    raise ValueError("Unknown type of default value.")


@overload
def get(key: str, default: None = None, raise_error=False,
        separator=',', item_factory=str, encoding='utf-8') -> str: ...


@overload
def get(key: str, default: T, raise_error=False,
        separator=',', item_factory=str, encoding='utf-8') -> T: ...


def get(key: str, default=None, raise_error=False,
        separator=',', item_factory=str, encoding='utf-8') -> T:
    """Autodetect right type based on default."""
    if default is None:
        return get_str(key, default, raise_error)
    if not isinstance(default, (int, float, bool, str, bytes, list)):
        raise ValueError('Bad type of default value.')
    return based_on_default(key, default, raise_error, separator=separator,
                            item_factory=item_factory, encoding=encoding)
