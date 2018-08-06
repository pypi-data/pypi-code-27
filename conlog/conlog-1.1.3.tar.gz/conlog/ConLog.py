import bitmath
import logging
import logging.handlers
import yaml


class ConLog(object):
    """Helper class to configure Logger instances. This class
    is used by `conlog.start` and should never need to be
    directly referenced unless debugging.
    """

    def __init__(self, **kwargs):
        """Setup attrubutes to be used by the root Logger.
        This should only be called from `conlog.start`.
        """
        self.yaml_file = kwargs['yaml_file']
        self.level = kwargs['level']
        self.log_format = kwargs['log_format']
        self.debug_format = kwargs['debug_format']
        self.log_file = kwargs['log_file']
        self.max_file_size = kwargs['max_file_size']
        self.max_retention = kwargs['max_retention']

        if self.yaml_file is not None:
            try:
                with open(self.yaml_file, 'r') as y_file:
                    y = yaml.load(y_file)['conlog']
                self.update_attrs(y)  # Update instance attrs with YAML values
            except KeyError:
                raise KeyError('"conlog" was not found in {}'.format(kwargs))

        self.update_attrs(kwargs)  # Update instance attributes

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
        """Configure and return the root Logger instance.
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
