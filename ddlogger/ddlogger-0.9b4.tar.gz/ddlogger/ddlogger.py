from __future__ import print_function
import sys
import contextlib


class DotDotLogger(object):
    """
    Prints dot to stdout so as to record the progress.
    """
    def __init__(self, dot='.', ncol=79, immediate_flush=True):
        """
        :param dot: the character to denote the dot
        :type dot: str
        :param ncol: the maximum number of dots per row, and if not positive or
               ``None``, then no upper limit
        :param immediate_flush: True to flush immediately
        """
        self.dot = dot
        self.ncol = None if ncol <= 0 else ncol
        self.cpos = 0
        self.immediate_flush = immediate_flush
        self.__logged_once = False

    def update(self):
        """
        Prints one dot.
        """
        if self.ncol and self.__logged_once and not self.cpos:
            sys.stdout.write('\n')
        sys.stdout.write(self.dot)
        if self.ncol:
            self.cpos = (self.cpos + 1) % self.ncol
        if self.immediate_flush:
            sys.stdout.flush()
        self.__logged_once = True


@contextlib.contextmanager
def ddlogger(**kwargs):
    """
    Context manager that added new line to the end of the log. All keyword
    arguments are passed directly to the constructor of ``DotDotLogger``.

    :yield: a ``DotDotLogger`` instance

    >>> from ddlogger import ddlogger
    >>> with ddlogger(dot='x', ncol=5) as dl:
    ...     for item in range(10):
    ...         # do something
    ...         dl.update()
    xxxxx
    xxxxx
    >>> with ddlogger(dot='x', ncol=6) as dl:
    ...     for item in range(10):
    ...         # do something
    ...         dl.update()
    xxxxxx
    xxxx
    """
    yield DotDotLogger(**kwargs)
    print()
