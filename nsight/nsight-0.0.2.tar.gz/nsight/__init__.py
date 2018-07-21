'''
nsight

Determine services on a server and possible pivots for pentesting
'''

__title__ = 'nsight'
__version__ = '0.0.2'
__all__ = ()
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2018 Johan Nestaas'

from .sudo import can_sudo
from .netstat import netstat, print_netstat


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--netstat', '-n', action='store_true')
    parser.add_argument('--sudo', '-s', action='store_true')
    args = parser.parse_args()

    use_sudo = False
    if args.sudo:
        if can_sudo():
            use_sudo = True
        else:
            print('warning: sudo failed, not using sudo')

    if args.netstat:
        netstats = netstat(use_sudo=use_sudo)
        print_netstat(netstats)


if __name__ == '__main__':
    main()
