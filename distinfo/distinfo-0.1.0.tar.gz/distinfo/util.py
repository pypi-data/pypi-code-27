from functools import partial
import json
import sys

from munch import unmunchify

import yaml

DUMPERS = dict(
    json=partial(json.dumps, default=str, sort_keys=True, indent=2),
    yaml=partial(yaml.dump, default_flow_style=False),
    yamls=yaml.dump,
)


def _todict(obj):
    result = dict()
    for key, value in obj.items():
        if isinstance(value, dict):
            value = _todict(value)
        if isinstance(value, set):
            value = sorted(map(str, value))
        result[key] = value
    return unmunchify(result)


def dumps(obj, fmt=None, **kwargs):
    if fmt is None:
        fmt = "json"
    return DUMPERS[fmt](_todict(obj), **kwargs)


def dump(obj, file=None, **kwargs):
    if file is None:
        file = sys.stdout
    print(dumps(obj, **kwargs), file=file)
