from time import mktime, strptime

import pytz
from datetime import datetime
from django.utils import timezone

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7


def local_time_to_utc(dt, tz=None):
    """
    Change local time to utc
    :param dt: datetime object
    :param tz: string with timezone name. ex. 'Europe/Berlin'. If None, will get current timezone
    :return: datetime object in utc timezone
    """
    local_timezone = pytz.timezone(tz) if tz else timezone.get_current_timezone()
    localized_datetime = local_timezone.localize(dt, is_dst=None)
    return localized_datetime.astimezone(pytz.utc)


def string_to_datetime(string_date, pattern):
    """
    String to datetime based on pattern
    :param string_date: date time in string
    :param pattern: time pattern, Example pattern: %Y-%m-%dT%H:%M:%S.%fZ
    :return: datetime object
    """
    return datetime.fromtimestamp(mktime(strptime(string_date, pattern)))
