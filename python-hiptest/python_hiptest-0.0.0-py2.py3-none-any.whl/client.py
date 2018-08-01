#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""hiptest.client

.. codeauthor:: John Lane <jlane@fanthreesixty.com>

"""

from six import string_types
import requests
from hiptest.models.project import *


class Hiptest(object):
    """Hiptest API client instance
    """

    def __init__(self, **kwargs):
        """Create a hiptest instance

        :param str access_token: Access token
        :param str client: Client ID
        :param str uid: User ID
        """

        self.base_url = "https://app.hiptest.com/api"
        self.session = requests.Session()
        self.headers = {'Accept': "application/vnd.api+json; version=1"}

        for item in kwargs:
            if isinstance(kwargs[item], str):
                self.headers[item.replace('_', '-')] = kwargs[item]

    @staticmethod
    def _verify_digit(value):
        """Raises an error if value is not an integer

        :param str value:
        :return:
        """

        if not isinstance(value, (string_types, int)) or not str(value).isdigit():
            raise TypeError("Error: %s is not an integer" % str(value))

    def get_projects(self):
        """Return the projects for a client

        :return:
        """

        result = self.session.get(self.base_url + "/projects", headers=self.headers)
        data = result.json() if result.ok else {"data": []}

        return [Project(**item) for item in data["data"]]

    def get_project(self, project_id):
        """Return project details

        :param str project_id: Hiptest project id
        :return:
        """

        self._verify_digit(project_id)
        result = self.session.get(self.base_url + "/projects/" + project_id, headers=self.headers)
        data = result.json() if result.ok else {"data": []}

        return ProjectDetail(**data)

    def create_project_backup(self, project_id):
        """Creates backup of project

        :param str project_id: Hiptest project id
        :return:
        """

        self._verify_digit(project_id)
        result = self.session.post(self.base_url + "/projects/" + project_id + "/backups", headers=self.headers)
        data = result.json() if result.ok else {"data": []}

        return ProjectDetail(**data)
