import structlog
import logging
import sys
from pythonjsonlogger import jsonlogger


_json_formatter = jsonlogger.JsonFormatter()
_text_formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s")

_handler = logging.StreamHandler()
_handler.setFormatter(_json_formatter)  # default formatter


def _dict_to_log(d):
    """
    Recursively create log in key=value pairs (text format)
    output for nested dictionaries.
    """
    arr = []
    for k, v in d.iteritems():
        val = v
        if isinstance(v, dict):
            val = '[{}]'.format(_dict_to_log(v))
        arr.append('{}={}'.format(k, val))
    return ' '.join(arr)


def _add_kwargs(logger, method_name, event_dict):
    """
    Add **kwargs to text format output
    """
    if _handler.formatter != _text_formatter:
        return event_dict

    d = dict(event_dict)
    del d['event']
    del d['level']
    del d['timestamp']
    event_dict['event'] = event_dict['event'] + ' ' + _dict_to_log(d)
    return event_dict


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        _add_kwargs,
        structlog.stdlib.render_to_log_kwargs,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

_logger = logging.getLogger()
_logger.addHandler(_handler)
_logger.setLevel(logging.DEBUG)

_log = structlog.get_logger()

_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR,
}


def set_format(fmt):
    """
    Set the log format

    :param string fmt: "json" or "text"
    """
    if fmt == "text":
        _handler.setFormatter(_text_formatter)
    else:
        _handler.setFormatter(_json_formatter)


def set_level(lvl):
    """
    Set the log level

    :param string lvl: "debug", "info", "warn" or "error"
    """
    _logger.setLevel(_levels[lvl])


def debug(msg, *args, **kwargs):
    """
    Log a message with level 'debug'
    """
    try:
        _log.debug(msg, *args, **kwargs)
    except Exception as e:
        _log.debug(msg, log_error=e)


def info(msg, *args, **kwargs):
    """
    Log a message with level 'info'
    """
    try:
        _log.info(msg, *args, **kwargs)
    except Exception as e:
        _log.info(msg, log_error=e)


def warn(msg, *args, **kwargs):
    """
    Log a message with level 'warn'
    """
    try:
        _log.warn(msg, *args, **kwargs)
    except Exception as e:
        _log.warn(msg, log_error=e)


def error(msg, *args, **kwargs):
    """
    Log a message with level 'error'
    """
    try:
        _log.error(msg, *args, **kwargs)
    except Exception as e:
        _log.error(msg, log_error=e)
