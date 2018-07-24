#!/usr/bin/python
# -*- coding: utf-8 -*-

from ..client import EDBOWebApiClient


class TestEDBOWebApiConnector(object):
    def setup(self):
        self.client = EDBOWebApiClient()

    def test_entrance_specialities_list(self):
        specialities = self.client.entrance_specialities_list({
            'filters': [],
            'governanceTypeId': self.client.get_university_info('governanceTypeId'),
            'menuItemCode': 'ENT_NZ4_UniversitySpecialities',
            'pageNo': 0,
            'pageSize': 100,
            'parentUniversityId': self.client.get_university_info('parentId'),
            'universityCode': self.client.get_university_info('code'),
            'universityId': self.client.get_university_info('universityId'),
        })

        assert isinstance(specialities, list)

    def test_get_status(self):
        assert isinstance(self.client.get_status(), int)

    def test_get_execution_time(self):
        assert isinstance(self.client.get_execution_time(), float)
