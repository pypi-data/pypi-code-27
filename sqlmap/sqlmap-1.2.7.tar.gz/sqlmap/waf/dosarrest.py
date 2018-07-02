#!/usr/bin/env python

"""
Copyright (c) 2006-2018 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.enums import HTTP_HEADER
from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "DOSarrest (DOSarrest Internet Security)"

def detect(get_page):
    retval = False

    for vector in WAF_ATTACK_VECTORS:
        _, headers, _ = get_page(get=vector)
        retval = re.search(r"DOSarrest", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
        retval |= headers.get("X-DIS-Request-ID") is not None
        if retval:
            break

    return retval
