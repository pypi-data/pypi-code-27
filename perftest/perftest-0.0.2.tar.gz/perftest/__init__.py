'''
perftest

Profiling and performance tests, made like unit testing.
'''

__title__ = 'perftest'
__version__ = '0.0.2'
__all__ = ('Loader', 'Module', 'Suite')
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2018 Johan Nestaas'

from .loader import Loader, Module
from .suite import Suite


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('root', nargs='?', default='.')
    args = parser.parse_args()

    load = Loader(root=args.root)
    load.run()


if __name__ == '__main__':
    main()
