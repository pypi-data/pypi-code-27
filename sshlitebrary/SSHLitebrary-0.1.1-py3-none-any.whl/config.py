from .utils import is_bytes, secs_to_timestr, timestr_to_secs

class ConfigurationException(Exception):
    """Raised when creating, updating or accessing a Configuration entry fails.
    """
    pass

class Configuration(object):
    def __init__(self, **entries):
        self._config = entries

    def __str__(self):
        return '\n'.join('%s=%s' % (k, v) for k, v in self._config.items())

    def update(self, **entries):
        for name, value in entries.items():
            if value is not None:
                self._config[name].set(value)

    def get(self, name):
        return self._config[name]

    def __getattr__(self, name):
        if name in self._config:
            return self._config[name].value
        msg = "Configuration parameter '%s' is not defined." % name
        raise ConfigurationException(msg)


class Entry(object):
    def __init__(self, initial=None):
        self._value = self._create_value(initial)

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    def set(self, value):
        self._value = self._parse_value(value)

    def _parse_value(self, value):
        raise NotImplementedError

    def _create_value(self, value):
        if value is None:
            return None
        return self._parse_value(value)


class StringEntry(Entry):
    def _parse_value(self, value):
        return str(value)


class IntegerEntry(Entry):
    def _parse_value(self, value):
        return int(value)


class TimeEntry(Entry):
    def _parse_value(self, value):
        value = str(value)
        return timestr_to_secs(value) if value else None

    def __str__(self):
        return secs_to_timestr(self._value)


class LogLevelEntry(Entry):
    LEVELS = ('TRACE', 'DEBUG', 'INFO', 'WARN', 'NONE')

    def _parse_value(self, value):
        value = str(value).upper()
        if value not in self.LEVELS:
            raise ConfigurationException("Invalid log level '%s'." % value)
        return value


class NewlineEntry(Entry):
    def _parse_value(self, value):
        if is_bytes(value):
            value = value.decode('ASCII')
        value = value.upper()
        return value.replace('LF', '\n').replace('CR', '\r')

