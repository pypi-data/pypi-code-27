import sys


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

    def update(self):
        """
        Prints one dot.
        """
        if self.ncol:
            self.cpos = (self.cpos + 1) % self.ncol
            if not self.cpos:
                sys.stdout.write('\n')
        sys.stdout.write(self.dot)
        if self.immediate_flush:
            sys.stdout.flush()
