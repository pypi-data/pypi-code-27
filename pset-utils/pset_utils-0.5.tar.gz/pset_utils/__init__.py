"""
A module that provides useful functionality for pyplot.

The `Figure` class will allow you to use
```
with Figure(name, figsize=figsize) as fig:
    # plot things
```
to easily display or save plots.

`Figure.set_interactive(False)` will cause `Figure`s to be saved on close.
To set the file extension for saved figures, use `Figure.set_extension(suffix)`

Note that if a non-default matplotlib backend is selected, it must be done
before loading this module.

To use monochromatic lines:
    pyplot.rcParams.update(monochrome_params)

To use the same font as the host document in embeded pgf:
    pyplot.rcParams.update(pgf_params)
"""
import contextlib
from cycler import cycler
import csv
import numpy as np
from matplotlib import pyplot as plt
import sys

# print monochromatic lines
monochrome = (cycler('marker', ['', '.']) *
              cycler('color', ['k', '0.5']) *
              cycler('linestyle', ['-', '--', ':', '-.']))
monochrome_params = {'axes.prop_cycle': monochrome}

# set up matplotlib for pgf export
pgf_params = {
        'font.family': 'serif',
        'font.serif': [],
        'font.sans-serif': [],
        'text.usetex': True
}

# default figure size
FIGSIZE = (6, 6)

class Figure(contextlib.AbstractContextManager):
    """A context manager to create and display or save a figure."""

    _interactive = True
    _number = 0
    _suffix = ''

    def __init__(self, *args, **kwargs):
        if not args:
            self.name = self._number
            Figure._number += 1
        elif isinstance(args[0], str):
            self.name = args[0]
            args = args[1:]
        else:
            self.fig = plt.figure()
            with self:
                plt.plot(*args, **kwargs)
            return
        if 'figsize' not in kwargs:
            kwargs['figsize'] = FIGSIZE
        self.fig = plt.figure(*args, **kwargs)

    def __enter__(self):
        return self.fig

    def __exit__(self, *args):
        if self._interactive:
            plt.show()
        else:
            self.fig.savefig(self.name + self._suffix)
            plt.close(self.fig)

    @classmethod
    def set_interactive(cls, interactive):
        """Sets whether the Figure is used in an interactive context."""
        cls._interactive = interactive

    @classmethod
    def set_extension(cls, suffix):
        """Sets the extension to be used when saving files.

        A value of `None` disables the addition of extensions.
        """
        cls._suffix = '.{}'.format(suffix) if suffix is not None else ''

    @classmethod
    def fig_3d(cls, *args, **kwargs):
        """Returns a `Figure3d` instance"""
        return Figure3d(*args, **kwargs)


class Figure3d(Figure):
    """A context manager to create and display or save a 3d figure."""

    def __enter__(self):
        return self.fig.add_subplot(1, 1, 1, projection="3d")


def figure_setup(pyplot, interactive=True, suffix=None):
    print("This function has been removed. "
          "Simply use the `Figure` class provided in this module.",
          file=sys.stderr)

def numpy_from_csv(filename, quoting=csv.QUOTE_NONNUMERIC, **kwargs):
    """Load a csv file into a numpy structured array.

    Args:
        filename: The filename to read from
        quoting (optional): The quoting option for csv.reader. Defaults to
            csv.QUOTE_NONNUMERIC.
        **kwargs (optional): Additional keyword arguments to pass to csv.reader

    Returns:
        A numpy structured array, with field names corresponding to the first
        row of the csv file. The dtype of each field is determined by the first
        row of data, with nonnumeric types given the object dtype (this allows
        the array to hold arbitrarily long strings, for example).
    """
    with open(filename) as f:
        data = list(csv.reader(f, quoting=quoting, **kwargs))
    dtypes = [type(x) if isinstance(x, (int, float)) else object for x in data[1]]
    return np.array([tuple(x) for x in data[1:]], dtype=list(zip(data[0], dtypes)))

