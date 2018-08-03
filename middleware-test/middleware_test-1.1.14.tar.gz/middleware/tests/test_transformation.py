import datetime
import json
import unittest
import uuid

import model
from components.transformation import DataDeliveryProcess
from tests.parent import BaseTestCase


class TestIternalModel(BaseTestCase):
    user = None
    data = {}

    @classmethod
    def setUpClass(cls):
        data = {
            "first_name": "Test_Fname",
            "last_name": "Test_Lname",
            "login": "Test_login",
            "email": "test_email@test.com",
            "skype": "Test_skype",
            "phone": "0000000000",
            "street": "Test_street",
            "city": "Test_city",
            "country": "Test_country",
            "company_name": "test_company",
            "description": "Test_description",
            "company_city": "Test_city",
            "company_street": "Test_street",
            "updated_at": "2018-02-07 12:27:51+00:00",
            "title": "TS"
        }
        user_id = model.ActiveDirectoryUser.add_active_directory_user(data["first_name"], data["last_name"],
                                                                      data["login"], data["email"], json.dumps(data))
        model.ActualUserData.add_actual_user_data(user_id, json.dumps(data))
        cls.data = data
        cls.user = model.ActiveDirectoryUser.find(email="test_email@test.com")[0]

    @staticmethod
    def add_write_cfg(params):
        return model.FieldWriteConfiguration.insert(field_write_configuration_id=uuid.uuid4().hex,
                                                    create_dttm=datetime.datetime.now(), **params)

    def test_ad_data(self):
        # create config
        TestIternalModel.add_write_cfg({"system_id": 1, "from_field_name": "updated_at", "to_path": "$.whenChanged",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 1, "from_field_name": "street",
                                        "to_path": "$.streetAddress",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 1,
                                        "from_field_name": "country",
                                        "to_path": "$.physicalDeliveryOfficeName",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 1,
                                        "from_field_name": "phone",
                                        "to_path": "$.mobile",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 1,
                                        "from_field_name": "company",
                                        "to_path": "$.company",
                                        "active": 1})

        actual = DataDeliveryProcess("0").transform("1", self.user, self.data)
        expected = {"co": "Test_country", "description": "Test_description", "mobile": "0000000000",
                    "userPrincipalName": "Test_login", "st": "Test_city", "streetAddress": "Test_street",
                    "sn": "Test_Lname", "physicalDeliveryOfficeName": "Test_country", "givenName": "Test_Fname"}

        self.assertDictEqual(actual, expected)

    def test_slack_data(self):
        TestIternalModel.add_write_cfg({"system_id": 2,
                                        "from_field_name": "title",
                                        "to_path": "$.profile.title",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 2,
                                        "from_field_name": "skype",
                                        "to_path": "$.profile.skype",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 2,
                                        "from_field_name": "phone",
                                        "to_path": "$.profile.phone",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 2,
                                        "from_field_name": "phone",
                                        "to_path": "$.profile.phone",
                                        "active": 1})
        actual = DataDeliveryProcess("0").transform("2", self.user, self.data)
        expected = {"profile": {"first_name": "Test_Fname", "last_name": "Test_Lname", "title": "TS",
                                "updated": "2018-02-07 12:27:51+00:00", "phone": "0000000000",
                                "skype": "Test_skype", "email": "test_email@test.com"}}

        self.assertDictEqual(actual, expected)

    def test_custom_system(self):
        # create config
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "first_name",
                                        "to_path": "$.user.first_name",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "login",
                                        "to_path": "$.user.login",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "country",
                                        "to_path": "$.user.address.country",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "city",
                                        "to_path": "$.user.address.city",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "street",
                                        "to_path": "$.user.address.street",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "phone",
                                        "to_path": "$.user.contacts.phone",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "email",
                                        "to_path": "$.user.contacts.email",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "skype",
                                        "to_path": "$.user.contacts.skype",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "company_name",
                                        "to_path": "$.user.company.name",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "company_city",
                                        "to_path": "$.user.company.address.company_city",
                                        "active": 1})
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "company_street",
                                        "to_path": "$.user.company.address.company_street",
                                        "active": 1})

        # test bad from field
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "bad_field",
                                        "to_path": "$.some_field",
                                        "active": 1})
        # test wrong system
        TestIternalModel.add_write_cfg({"system_id": 10,
                                        "from_field_name": "first_name",
                                        "to_path": "$.user.profile.first_name",
                                        "active": 1})
        # test not active field
        TestIternalModel.add_write_cfg({"system_id": 5,
                                        "from_field_name": "skype",
                                        "to_path": "$.user.profile.skype",
                                        "active": 0})

        actual = DataDeliveryProcess("0").transform("5", self.user, self.data)
        expected = {"user": {"login": "Test_login", "company": {"name": "test_company",
                                                                "address": {"company_city": "Test_city",
                                                                            "company_street": "Test_street"}},
                             "contacts": {"phone": "0000000000", "email": "test_email@test.com",
                                          "skype": "Test_skype"}, "first_name": "Test_Fname",
                             "address": {"country": "Test_country", "street": "Test_street", "city": "Test_city"}}}

        self.assertDictEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
