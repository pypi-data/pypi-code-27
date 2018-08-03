"""The version of thermohw."""
from typing import Tuple

__version_info__: Tuple[int, int, int, str] = (0, 2, 0, 'dev1')
__version__ = '.'.join(map(str, __version_info__))
