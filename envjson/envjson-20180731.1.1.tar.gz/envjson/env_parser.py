import json
import os
from typing import Optional, Union

NOTSET = object()

_env_json_types = (dict, list, int, float, bool, None)
_env_types = (str, ) + _env_json_types


def _env(name: str, default: Union[_env_types]=NOTSET) -> Union[_env_types]:
    try:
        return os.environ[name]
    except KeyError:
        if default is NOTSET:
            raise
        return default

# core methods


def env_str(
        name: str,
        default: Optional[str]=NOTSET) -> Optional[str]:
    return _env(name, default)


def env_json(name: str,
             default: Union[_env_json_types]=NOTSET,
             parsetype: type = object) -> Union[_env_json_types]:
    assert parsetype is not None
    if default is NOTSET:
        default_json = NOTSET
    else:
        default_json = json.dumps(default)
    value = json.loads(_env(name, default_json))
    if not isinstance(value, parsetype):
        raise ValueError(
            "Env json var '%s' is not %s" % (name, parsetype.__name__))
    return value


# helpers

def env_json_bool(name: str, default: bool=NOTSET) -> bool:
    return bool(env_json(name, default, parsetype=bool))


def env_json_int(name: str, default: int=NOTSET) -> int:
    return env_json(name, default, parsetype=int)
