"""
Extension for generating Sphinx and LaTeX documentation with embedded notation.
"""


class AbjadBookError(Exception):
    '''
    An abjad-book error.
    '''
    pass


from ._version import __version__, __version_info__  # noqa
from .specifiers import *  # noqa
from .proxies import *  # noqa
from .directives import *  # noqa
from . import sphinx  # noqa

from .AbjadBookConsole import AbjadBookConsole  # noqa
from .AbjadBookScript import AbjadBookScript  # noqa
from .CodeBlock import CodeBlock  # noqa
from .LaTeXDocumentHandler import LaTeXDocumentHandler  # noqa
from .LilyPondBlock import LilyPondBlock  # noqa
from .SphinxDocumentHandler import SphinxDocumentHandler  # noqa
from .example_function import example_function  # noqa
