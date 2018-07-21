# standard library
import logging
import traceback


class DbLogHandler(logging.Handler):
    """
    Custom log handler
    """

    def __init__(self, model=''):
        super(DbLogHandler, self).__init__()

    def emit(self, record):
        from .models import DBLogEntry

        if record.exc_info:
            trace = traceback.format_exc()
        else:
            trace = None

            DBLogEntry.objects.create(
                level=record.levelname,
                message=record.getMessage(),
                trace=trace,
            )
