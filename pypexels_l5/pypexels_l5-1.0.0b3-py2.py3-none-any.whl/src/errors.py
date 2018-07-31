from __future__ import unicode_literals

from builtins import str, super


class PexelsError(Exception):
    def __init__(self, message):
        self.message = str(message) if message else 'Unknown error'
        super().__init__(message)

    def __str__(self):
        return self.message
