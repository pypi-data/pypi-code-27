#!/usr/bin/env python
import re

# Default timestamp regex
# Will be imported and used by default for operations if none supplied.

# With optional milleseconds `msec`
# Matches something like "2015-05-16 05:40:20,125"
RE_TIMESTAMP = re.compile(
    r'(?P<year>\d\d\d\d)-'
    r'(?P<month>\d\d)-'
    r'(?P<day>\d\d)\s+'
    r'(?P<time>\d\d:\d\d:\d\d)'
    r'(?:,(?P<msec>\d\d\d))?'
)

