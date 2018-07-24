"""

#############
conlog
#############

Anti-Boilerplate Console Logging Module for Python


About
=====

``conlog`` is a configurable console logging mechanism featuring,

  * Boilerplate-free setup
      + Setup in only one line per Logger
  * Export to optional rotating log file
  * Log verbosity based on logging level
      + Show additional columns when debugging, suppress columns when not
  * YAML or argument based configuration


Documentation
=============

Documentation is available `here <https://github.com/RyanMillerC/conlog>`_.

"""


import bitmath
import logging
import logging.handlers
import yaml


class ConLog(object):
    """Helper class to configure Logger instances.
    """

    def __init__(self, conf={}):
        self.yaml_file = None
        self.level = 'INFO'
        self.log_format = '%(asctime)22s - %(levelname)8s - %(name)20s - ' \
                          '%(message)s'
        self.debug_format = '%(asctime)22s - %(levelname)8s - %(name)20s - ' \
                            '%(funcName)20s - %(message)s'
        self.log_file = None
        self.max_file_size = 5000000
        self.max_retention = 5

        if 'yaml_file' in conf:
            self.yaml_file = conf['yaml_file']
            try:
                with open(self.yaml_file, 'r') as y_file:
                    y = yaml.load(y_file)['conlog']
                self.update_attrs(y)  # Update instance attrs with YAML values
            except KeyError:
                raise KeyError('"conlog" was not found in {}'.format(conf))

        self.update_attrs(conf)  # Update instance attributes with user values

    def update_attrs(self, d):
        """Update ConLog instance attributes with new values from
        a dictionary.

        :param dict d:
            Dictionary of user supplied option overrides
        """
        if 'level' in d:
            self.level = d['level']
        if 'log_format' in d:
            self.log_format = d['log_format']
        if 'debug_format' in d:
            self.debug_format = d['debug_format']
        if self.level == 'DEBUG':
            self.log_format = self.debug_format
        if 'log_file' in d:
            self.log_file = d['log_file']
            if 'max_file_size' in d:
                try:  # Convert value to bytes
                    self.max_file_size = int(
                        bitmath.parse_string(d['max_file_size']).bytes
                    )
                except ValueError:  # Value is supplied is in bytes
                    self.max_file_size = int(d['max_file_size'])
            if 'max_retention' in d:
                self.max_retention = d['max_retention']

    def setup_root_logger(self):
        """Configure and return a root Logger instance.
        """
        logger = logging.getLogger()
        logger.setLevel(self.level)
        formatter = logging.Formatter(self.log_format)

        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if self.log_file:
            fh = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_file_size,
                backupCount=self.max_retention
            )
            fh.setLevel(self.level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        return logger


def new(inst):
    """Get a new Logger instance for the calling class. Recommended
    usage is ``self.log = conlog.new(self)``

    :param object inst:
        Instance of class which new Logger is for (use ``self``).
    """
    return logging.getLogger(inst.__class__.__name__)


def start(**kwargs):
    """Configure and return the root Logger instance. All arguments
    are optional. If any argument is not supplied, its default
    value be used. It is even possible to run with no arguments,
    in which case the default values would be used across all
    options.

    :param yaml_file:
        Default: ``None``

        Pull configurations from YAML file. All option entries should
        be nested under ``conlog`` at the root of the YAML file. All
        parameters from ``start()`` are available as YAML options. The
        file, at it's root level, should be structured:
        ::

            conlog:
              file: log/app.log
              format: '%(asctime)22s - %(levelname)8s - %(name)20s - %(message)s'
              debug_format: '%(asctime)22s - %(levelname)8s - %(name)20s - %(funcName)20s - %(message)s'
              level: INFO
              max_file_size: 5 MB
              max_retention: 5

        Like ``start()`` parameters, all YAML settings are optional.
        If any setting is not supplied in the configuration, its
        default value will be used.

        If ``yaml_file`` is supplied, its values are processed first,
        and will be overridden by any additional parameters called in
        ``start()``

    ``log_file``
        Default: ``None``

        Path to log file. By default, file logging is disabled. If
        ``log_file`` is set to a file path, for example, ``log/app.log``,
        it will enable rotating file logging.

        NOTE: In the example ``log/app.log``, the log file itself,
        ``app.log``, does not need to exist; however, the base directory
        ``log`` MUST exist.

        By default the log file will rotate when it reaches ``5 MB``,
        with up to ``5`` rotations being kept before overwriting the oldest.
        These values can be adjusted using the ``max_file_size`` and
        ``max_retention`` options.

    :param log_format:
        Default: ``%(asctime)22s - %(levelname)8s - %(name)20s - %(message)s``

        Logging format for all levels EXCEPT ``DEBUG``.

    :param debug_format:
        Default: ``%(asctime)22s - %(levelname)8s - %(name)20s - %(funcName)20s - %(message)s``

        Logging format for ``DEBUG`` level. By default, this displays the
        same formatting as ``format``, but with an additional column for
        the function name which is calling the Logger.

    :param level:
        Default: ``INFO``

        Logging level. Only messages sent to this level or higher will
        appear in log.

    :param max_file_size:
        Default: ``5 MB``

        Maximum log file size before rollover. This value can either
        be an integer byte size or a proper string like: ``5 MB``,
        ``50 kB``, etc. Setting to ``0`` will cause the log file to
        grow infinitely with no rollover. This option has no impact if
        ``file`` is set to ``None``.

    :param max_retention:
        Default: ``5``

        Maximum number of rollover logs to keep. Rotated logs will be
        saved in the format ``log_name.1``, ``log_name.2``, etc.,
        until ``max_retention`` is reached. At that point the oldest
        of the rollover logs will be purged. This option has no impact
        if ``file`` is set to ``None``, or if ``max_file_size`` is set
        to ``0``.
    """
    cl = ConLog(kwargs)
    logger = cl.setup_root_logger()
    return logger
