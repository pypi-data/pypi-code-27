import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        # Set timestamp
        now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        log_record['timestamp'] = log_record.get('timestamp', now)
        # Set severity
        severity = log_record.get("level", record.levelname)
        log_record['severity'] = severity.upper()
        # Set sourceLocation
        source_location = {
            "file": record.filename,
            "function": record.funcName,
            "line": record.lineno,
            "loggerName": record.name,
            "threadName": record.threadName,
            "thread": record.thread,
        }
        log_record["sourceLocation"] = source_location


def configure_logger(logger_name: str, log_level: str, log_json: bool,
                     replace_handler: bool = True, filters=None):
    """
    Configure logger
    :param logger_name: Name of the logger. None for root logger.
    :param log_json: bool Flag for logging json or not
    :param log_level: Log level. E.g. "DEBUG"
    :param filters: List of filters to add to log handler.
    :return: Logger
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    if replace_handler:
        logger.handlers = []
        logger.propagate = False
    log_handler = logging.StreamHandler()
    if log_json:
        formatter = CustomJsonFormatter()
        log_handler.setFormatter(formatter)
    else:
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(threadName)s. %(message)s (%(filename)s:%(lineno)s)",
            "%Y-%m-%d %H:%M:%S",
        )
        log_handler.setFormatter(formatter)
    if filters and isinstance(filters, list):
        for filter in filters:
            log_handler.addFilter(filter)

    logger.addHandler(log_handler)

    return logger
