#!/usr/bin/env python3

from .boto_args import args
from .boto_config_file import config_file
from .boto_env_vars import env_vars

import sys

def main():
    if len(sys.argv) == 3:
        args()
    elif len(sys.argv) == 2 and sys.argv[1] == '--config':
        config_file()
    elif len(sys.argv) == 1:
        env_vars()
    else:
        print('Usage:')
        print('\t' + sys.argv[0] + ' <id> <password>')
        print('\t' + sys.argv[0] + '           * reads credentials from'+
              ' environment variables.')
        print('\t' + sys.argv[0] + ' --config  * reads credentials from config file')

        sys.exit(1)

if __name__ == '__main__':
    main()
