""" Constants """
import json
OPTION_PRECEDENCE = ['cli', 'env', 'ini', 'dft']

OPTION_TYPE_MAP = {
    # 'protocol': str,
    'debug': str,
    'local_strategy': bool,
    'no_config_cache': bool,
    'no_config_sync': bool,
    'murano_host': str,
    'murano_id': str,
    'no_filesystem': bool,
    'config_io_file': str,
    'ini_file': str,
    'murano_token': str,
    'watchlist': list,
    'http_timeout': int,
    'certfile': str,
    'pkeyfile': str,
    'murano_cacert': str,
    'murano_port': int
}

OPTION_NAME_MAPPER = {
    'env': lambda d, x: d.get('EDGED_{}'.format(x.upper()), None),
    'cli': lambda d, x: d.get('--{}'.format(x.replace('_', '-')), None),
    'dft': lambda d, x: d.get(x, None),
    'ini': lambda d, x: d.get(x)
}

def _ini_get(I, string):
    try:
        s, o = string.split('.')
        if s in I.sections():
            return I.get(s, o)
        else:
            return None
    except:
        return None

DEFAULTS = {
    'protocol': 'http',
    'debug': 'CRITICAL',
    'local_strategy': False,
    'no_config_cache': False,
    'no_config_sync': False,
    'no_filesystem': False,
    'watchlist': ['config_io'],
    'http_timeout': 60*5*1000,
    'ini_file': 'default.ini'
}
