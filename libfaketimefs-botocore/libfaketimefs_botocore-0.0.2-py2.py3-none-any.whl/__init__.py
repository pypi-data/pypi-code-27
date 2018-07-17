import botocore.auth
import botocore.credentials
import datetime
import os

from dateutil.parser import parse


FAKETIME_REALTIME_FILE = os.environ.get('FAKETIME_REALTIME_FILE')


def real_time():
    with open(FAKETIME_REALTIME_FILE) as open_file:
        return float(open_file.read())


class PatchedDate(datetime.date):

    @classmethod
    def today(cls):
        t = real_time()
        return cls.fromtimestamp(t)


class PatchedDatetime(datetime.datetime):

    @classmethod
    def now(cls, tz=None):
        t = real_time()
        return cls.fromtimestamp(t, tz)

    @classmethod
    def utcnow(cls):
        t = real_time()
        return cls.utcfromtimestamp(t)


class PatchedDatetimeModule(object):
    """
    Wrapper for the datetime module that uses libfaketimefs's realtime file
    to determine the current time, rather than making a system call which
    would be intercepted by libfaketime.

    """

    date = PatchedDate
    datetime = PatchedDatetime

    def __getattr__(self, name):
        return getattr(self._datetime, name)


def patch_botocore():
    """
    Patches botocore to work while using libfaketime and libfaketimefs.

    """

    # Do nothing when not configured correctly.

    if not FAKETIME_REALTIME_FILE:
        return

    # Create a patched datetime module that bypasses libfaketime
    # and returns the real time.

    patched_datetime_module = PatchedDatetimeModule()

    # Patch the botocore.auth module.

    botocore.auth.datetime = patched_datetime_module

    # It looks like requests made using some older AWS signature versions
    # would require patching the following variables, but I'm not sure
    # how to test them so they haven't been patched.
    # * botocore.auth.formatdate for email.formatdate(usegmt=True)
    # * botocore.auth.time for time.gmtime() and time.time()

    # Patch the botocore.credentials module.

    botocore.credentials.datetime = patched_datetime_module

    def _parse_if_needed(value):
        if isinstance(value, datetime.datetime):
            return value
        return parse(value)

    botocore.credentials._parse_if_needed = _parse_if_needed

    def _serialize_if_needed(value, iso=False):
        if isinstance(value, datetime.datetime):
            if iso:
                return value.isoformat()
            return value.strftime('%Y-%m-%dT%H:%M:%S%Z')
        return value

    botocore.credentials._serialize_if_needed = _serialize_if_needed
