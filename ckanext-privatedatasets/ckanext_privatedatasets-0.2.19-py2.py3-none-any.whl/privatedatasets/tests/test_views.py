# -*- coding: utf-8 -*-

# Copyright (c) 2014 CoNWeT Lab., Universidad Politécnica de Madrid
# Copyright (c) 2018 Future Internet Consulting and Development Solutions S.L.

# This file is part of CKAN Private Dataset Extension.

# CKAN Private Dataset Extension is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN Private Dataset Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN Private Dataset Extension.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from mock import ANY, DEFAULT, MagicMock, patch
from parameterized import parameterized

from ckanext.privatedatasets import views


@patch.multiple("ckanext.privatedatasets", base=DEFAULT, toolkit=DEFAULT, model=DEFAULT, g=DEFAULT, logic=DEFAULT)
class ViewsTest(unittest.TestCase):

    @parameterized.expand([
        ('ObjectNotFound', 404),
        ('NotAuthorized', 401),
    ])
    def test_exceptions_loading_users(self, exception, expected_status, mocks):

        # Configure the mock
        user_show = MagicMock(side_effect=getattr(mocks['logic'], exception))
        mocks['toolkit'].get_action = MagicMock(return_value=user_show)

        # Call the function
        views.acquired_datasets()

        # Assertations
        expected_context = {
            'auth_user_obj': mocks['g'].userobj,
            'for_view': True,
            'model': mocks['model'],
            'session': mocks['model'].Session,
            'user': mocks['g'].user,
        }

        user_show.assert_called_once_with(expected_context, {'user_obj': mocks['g'].userobj})
        mocks['base'].abort.assert_called_once_with(expected_status, ANY)

    def test_no_error_loading_users(self, mocks):

        # actions
        default_user = {'user_name': 'test', 'another_val': 'example value'}
        user_show = MagicMock(return_value=default_user)
        acquisitions_list = MagicMock()

        def _get_action(action):
            if action == 'user_show':
                return user_show
            else:
                return acquisitions_list

        mocks['toolkit'].get_action = MagicMock(side_effect=_get_action)

        # Call the function
        returned = self.instanceUI.user_acquired_datasets()

        # User_show called correctly
        expected_context = {
            'auth_user_obj': mocks['g'].userobj,
            'for_view': True,
            'model': mocks['model'],
            'session': mocks['model'].Session,
            'user': mocks['g'].user,
        }

        user_show.assert_called_once_with(expected_context, {'user_obj': mocks['g'].userobj})
        acquisitions_list.assert_called_with(expected_context, None)

        # Check that the render method has been called
        mocks['base'].render.assert_called_once_with('user/dashboard_acquired.html', {'user_dict': expected_context, 'acquired_datasets': acquisitions_list})
        self.assertEqual(returned, mocks['base'].render())
