"""Network propagation on top of the networkx package."""

from .run import (  # noqa: F401
    run_experiments_by_dir,
)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
