import os
import sys
import logging
import logging.handlers
from logging_gelf.handlers import GELFUDPSocketHandler
from collections import defaultdict

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


class MultiLogger(logging.Handler):
    '''
    Python logger to handle logging to multiple destinations such as
    console, file and gelf
    '''

    def __init__(self, loggers, level='info'):

        logging.Handler.__init__(self)

        if 'level' in loggers:
            self.level = LOG_LEVELS[loggers['level'].upper()]
        else:
            self.level = LOG_LEVELS[level.upper()]

        if 'console' in loggers:
            self.console = loggers['console']
        else:
            self.console = defaultdict(None)

        if 'file' in loggers:
            self.file = loggers['file']
        else:
            self.file = defaultdict(None)

        if 'gelf' in loggers:
            self.gelf = loggers['gelf']
            if 'host' not in self.gelf:
                self.gelf['host'] = 'localhost'
            if 'port' not in self.gelf:
                self.gelf['port'] = 12021
        else:
            self.gelf = defaultdict(None)

    def getLogger(self):

        self._logger = logging.getLogger(os.path.basename(sys.argv[0]))

        self._logger.setLevel(self.level)
        format = logging.Formatter(
            '%(asctime)s %(name)s [%(levelname)s] %(message)s')

        if self.console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(format)
            if 'level' in self.console:
                console_level = LOG_LEVELS[self.console['level'].upper()]
                console_handler.setLevel(console_level)

            self._logger.addHandler(console_handler)

        if self.file:
            file_handler = logging.FileHandler(self.file['path'])
            file_handler.setFormatter(format)
            if 'level' in self.file:
                file_level = LOG_LEVELS[self.file['level'].upper()]
                file_handler.setLevel(file_level)

            self._logger.addHandler(file_handler)

        if self.gelf:
            gelf_handler = GELFUDPSocketHandler(host=self.gelf['host'],
                                                port=self.gelf['port'])
            if 'level' in self.gelf:
                gelf_level = LOG_LEVELS[self.gelf['level'].upper()]
                gelf_handler.setLevel(gelf_level)

            self._logger.addHandler(gelf_handler)

        return self._logger
