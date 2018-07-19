# Canopy product code
#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
from __future__ import absolute_import

from hatcher.core.url_templates import URLS_V1
from hatcher.core.v0.user import User as UserV0


class User(UserV0):

    def __init__(self, organization_name, email, url_handler, model_registry):
        super(User, self).__init__(
            organization_name, email, url_handler, model_registry)
        self._urls = URLS_V1
