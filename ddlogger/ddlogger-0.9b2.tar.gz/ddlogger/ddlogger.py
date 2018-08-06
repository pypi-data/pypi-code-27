import sys


class DotDotLogger(object):
    """
    Prints dot to stdout so as to record the progress.
    """
    def __init__(self, dot='.', ncol=79):
        """
        :param dot: the character to denote the dot
        :type dot: str
        :param ncol: the maximum number of dots per row
        :type ncol: int
        """
        self.dot = dot
        self.ncol = ncol
        self.cpos = 0

    def update(self):
        """
        Prints one dot.
        """
        self.cpos = (self.cpos + 1) % self.ncol
        if not self.cpos:
            sys.stdout.write('\n')
        sys.stdout.write(self.dot)
        sys.stdout.flush()
