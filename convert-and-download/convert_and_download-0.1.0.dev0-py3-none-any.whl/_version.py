"""The version of convert_and_download."""
from typing import Tuple

__version_info__: Tuple[int, int, int, str] = (0, 1, 0, 'dev')
__version__ = '.'.join(map(str, __version_info__))
