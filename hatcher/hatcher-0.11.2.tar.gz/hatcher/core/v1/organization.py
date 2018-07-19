# Canopy product code
#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
from __future__ import absolute_import

from hatcher.core.url_templates import URLS_V1
from hatcher.core.v0.organization import Organization as OrganizationV0


class Organization(OrganizationV0):
    """A representation of an organization in a Brood server.

       The object will use the V1 entrypoints.

    """

    def __init__(self, name, url_handler, model_registry):
        super(Organization, self).__init__(name, url_handler, model_registry)
        self._urls = URLS_V1  # Make sure that we use the V1 entry points
