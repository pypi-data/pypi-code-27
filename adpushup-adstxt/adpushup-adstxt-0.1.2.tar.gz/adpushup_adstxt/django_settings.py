# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
import os

API_USER_ID = getattr(settings, "ADPUSHUP_API_USER_ID", "")
API_KEY = getattr(settings, "ADPUSHUP_API_KEY", "")

WWW_DIR = getattr(
    settings, "ADPUSHUP_WWW_DIR", os.path.join(getattr(settings, "ROOT_DIR"), "www")
)
