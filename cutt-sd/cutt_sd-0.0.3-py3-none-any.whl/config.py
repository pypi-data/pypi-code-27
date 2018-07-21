import os

DEFAULT_ENV = 'cutt' if 'RUN_ENV' not in os.environ else os.environ['RUN_ENV']
DEFAULT_SERVER = os.environ['SD_SERVER'] if 'SD_SERVER' in os.environ else 'http://localhost:4367/'
