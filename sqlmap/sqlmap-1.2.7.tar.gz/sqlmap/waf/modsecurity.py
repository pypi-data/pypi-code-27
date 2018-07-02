#!/usr/bin/env python

"""
Copyright (c) 2006-2018 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import re

from lib.core.enums import HTTP_HEADER
from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "ModSecurity: Open Source Web Application Firewall (Trustwave)"

def detect(get_page):
    retval = False

    for vector in WAF_ATTACK_VECTORS:
        page, headers, code = get_page(get=vector)
        retval = re.search(r"Mod_Security|NOYB", headers.get(HTTP_HEADER.SERVER, ""), re.I) is not None
        retval |= any(_ in (page or "") for _ in ("This error was generated by Mod_Security", "One or more things in your request were suspicious", "rules of the mod_security module"))
        if retval:
            break

    return retval
