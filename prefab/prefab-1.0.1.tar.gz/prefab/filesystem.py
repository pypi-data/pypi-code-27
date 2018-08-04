import os
from typing import Any


def mkdirp(path: str, *args: Any, **kwargs: Any) -> None:
    try:
        os.makedirs(path, *args, **kwargs)
    except OSError:
        if not os.path.exists(path):
            raise
