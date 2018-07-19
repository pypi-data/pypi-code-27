# Canopy product code
#
# (C) Copyright 2013 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
from __future__ import absolute_import

from ..url_templates import URLS_V0


class User(object):

    def __init__(self, organization_name, email, url_handler, model_registry):
        self.organization_name = organization_name
        self.email = email
        self._url_handler = url_handler
        self._model_registry = model_registry
        self._urls = URLS_V0

    def __repr__(self):
        return '<{cls} organization={organization!r}, email={email!r}>'.format(
            cls=type(self).__name__,
            organization=self.organization_name,
            email=self.email,
        )

    def delete(self):
        """Delete this user from the brood server.

        """
        path = self._urls.admin.users.metadata.format(
            organization_name=self.organization_name,
            email=self.email,
        )
        self._url_handler.delete(path)

    def metadata(self):
        """Get the user's metadata.

        """
        path = self._urls.admin.users.metadata.format(
            organization_name=self.organization_name,
            email=self.email,
        )
        return self._url_handler.get_json(path)
