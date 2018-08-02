import datetime
import json
import unittest
import uuid

import model
from components.providers import Slack, ActiveDirectory, SelectHR
from components.service import GetInternalModel
from tests.parent import BaseTestCase


class TestInternalModel(BaseTestCase):
    user = model.ActiveDirectoryUser.find(email="yulia-knubisoft@octopuslabs.com")[0]
    ad_json = ActiveDirectory("1").__transform__(json.loads(user["metadata"]), user)
    slack_json = Slack("1").get_json(user)
    hr_json = SelectHR("1").get_json(user)
    map = {"1": ad_json, "2": slack_json, "3": hr_json}

    def test_start_with(self):
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id="2",
                                            from_path="$.user.profile.email",
                                            to_field_name="email",
                                            active=1, create_dttm=datetime.datetime.now())
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id="2",
                                            from_path="profile.first_name",
                                            to_field_name="first_name",
                                            active=1, create_dttm=datetime.datetime.now())

        actual = GetInternalModel(1, self.user["active_directory_user_id"]).get_model(self.map)
        expected = [{"system_id": "1",
                     "dictionary": {"last_name": "Probachai", "city": "Vinnitsya", "first_name": "Julia",
                                    "post_code": "21000", "display_name": "Yuliya Probachai",
                                    "updated_at": "2018-05-07T08:18:23+00:00", "home_page": "vk.com",
                                    "country": "Ukraine", "company": "Imagination",
                                    "mobile_phone_number": "+380995399849", "fax": "", "desk_number": "Ukraine",
                                    "work_phone_number": "+380672112999",
                                    "ad_path": "CN=Yuliya Probachai,OU=Test-Users,DC=test-octopus,DC=local",
                                    "manager": "", "street": "Litvinenko", "team": "", "middle_name": "blah",
                                    "login": "Yuliya.Probachai", "job_title": ""}}, {"system_id": "3",
                                                                                     "dictionary": {
                                                                                         "first_name": "Julia",
                                                                                         "last_name": "Probachai",
                                                                                         "middle_name": "",
                                                                                         "description": None,
                                                                                         "end_date": None,
                                                                                         "title": "XXX",
                                                                                         "updated_at": "2018-01-19T00:00:00",
                                                                                         "work_phone_number": "+380672112999",
                                                                                         "mobile_phone_number": "+380995399849",
                                                                                         "manager": None,
                                                                                         "person_number": 1,
                                                                                         "team": None,
                                                                                         "salutation": "Nkpm Tpoegk",
                                                                                         "email": "yulia-knubisoft@octopuslabs.com",
                                                                                         "job_title": None}},
                    {"system_id": "2",
                     "dictionary": {"status": "", "what_do": "Python Developer", "first_name": "Julia",
                                    "last_name": "Probachai", "display_name": "Julia Probachai",
                                    "photo": "https://avatars.slack-edge.com/2018-03-16/331289011283_b33239e4cb8e4d62ae6c_192.jpg",
                                    "updated_at": "2018-05-07T14:06:26+00:00", "linked_in": "http://www.example.com",
                                    "work_phone_number": "+380672112999", "mobile_phone_number": "+380995399849",
                                    "skype": "skype", "email": "yulia-knubisoft@octopuslabs.com",
                                    "job_title": "Python Developer"}}]

        self.assertListEqual(actual, expected)

    def test_bad_from_field(self):
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id=2,
                                            from_path="$.sdcvbvcxcv",
                                            to_field_name="some_field",
                                            active=1, create_dttm=datetime.datetime.now())
        actual = GetInternalModel(1, self.user["active_directory_user_id"]).get_model(self.map)
        expected = [{"system_id": "1",
                     "dictionary": {"last_name": "Probachai", "city": "Vinnitsya", "first_name": "Julia",
                                    "post_code": "21000", "display_name": "Yuliya Probachai",
                                    "updated_at": "2018-05-07T08:18:23+00:00", "home_page": "vk.com",
                                    "country": "Ukraine", "company": "Imagination",
                                    "mobile_phone_number": "+380995399849", "fax": "", "desk_number": "Ukraine",
                                    "work_phone_number": "+380672112999",
                                    "ad_path": "CN=Yuliya Probachai,OU=Test-Users,DC=test-octopus,DC=local",
                                    "manager": "", "street": "Litvinenko", "team": "", "middle_name": "blah",
                                    "login": "Yuliya.Probachai", "job_title": ""}}, {"system_id": "3",
                                                                                     "dictionary": {
                                                                                         "first_name": "Julia",
                                                                                         "last_name": "Probachai",
                                                                                         "middle_name": "",
                                                                                         "description": None,
                                                                                         "end_date": None,
                                                                                         "title": "XXX",
                                                                                         "updated_at": "2018-01-19T00:00:00",
                                                                                         "work_phone_number": "+380672112999",
                                                                                         "mobile_phone_number": "+380995399849",
                                                                                         "manager": None,
                                                                                         "person_number": 1,
                                                                                         "team": None,
                                                                                         "salutation": "Nkpm Tpoegk",
                                                                                         "email": "yulia-knubisoft@octopuslabs.com",
                                                                                         "job_title": None}},
                    {"system_id": "2",
                     "dictionary": {"status": "", "what_do": "Python Developer", "first_name": "Julia",
                                    "last_name": "Probachai", "display_name": "Julia Probachai",
                                    "photo": "https://avatars.slack-edge.com/2018-03-16/331289011283_b33239e4cb8e4d62ae6c_192.jpg",
                                    "updated_at": "2018-05-07T14:06:26+00:00", "linked_in": "http://www.example.com",
                                    "work_phone_number": "+380672112999", "mobile_phone_number": "+380995399849",
                                    "skype": "skype", "email": "yulia-knubisoft@octopuslabs.com",
                                    "job_title": "Python Developer"}}]

        self.assertListEqual(actual, expected)

    def test_custom_field(self):
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id=2,
                                            from_path="$.user.profile.skype",
                                            to_field_name="skype",
                                            active=1, create_dttm=datetime.datetime.now())
        actual = GetInternalModel(1, self.user["active_directory_user_id"]).get_model(self.map)
        expected = [{"system_id": "1",
                     "dictionary": {"last_name": "Probachai", "city": "Vinnitsya", "first_name": "Julia",
                                    "post_code": "21000", "display_name": "Yuliya Probachai",
                                    "updated_at": "2018-05-07T08:18:23+00:00", "home_page": "vk.com",
                                    "country": "Ukraine", "company": "Imagination",
                                    "mobile_phone_number": "+380995399849", "fax": "", "desk_number": "Ukraine",
                                    "work_phone_number": "+380672112999",
                                    "ad_path": "CN=Yuliya Probachai,OU=Test-Users,DC=test-octopus,DC=local",
                                    "manager": "", "street": "Litvinenko", "team": "", "middle_name": "blah",
                                    "login": "Yuliya.Probachai", "job_title": ""}}, {"system_id": "3",
                                                                                     "dictionary": {
                                                                                         "first_name": "Julia",
                                                                                         "last_name": "Probachai",
                                                                                         "middle_name": "",
                                                                                         "description": None,
                                                                                         "end_date": None,
                                                                                         "title": "XXX",
                                                                                         "updated_at": "2018-01-19T00:00:00",
                                                                                         "work_phone_number": "+380672112999",
                                                                                         "mobile_phone_number": "+380995399849",
                                                                                         "manager": None,
                                                                                         "person_number": 1,
                                                                                         "team": None,
                                                                                         "salutation": "Nkpm Tpoegk",
                                                                                         "email": "yulia-knubisoft@octopuslabs.com",
                                                                                         "job_title": None}},
                    {"system_id": "2",
                     "dictionary": {"status": "", "what_do": "Python Developer", "first_name": "Julia",
                                    "last_name": "Probachai", "display_name": "Julia Probachai",
                                    "photo": "https://avatars.slack-edge.com/2018-03-16/331289011283_b33239e4cb8e4d62ae6c_192.jpg",
                                    "updated_at": "2018-05-07T14:06:26+00:00", "linked_in": "http://www.example.com",
                                    "work_phone_number": "+380672112999", "mobile_phone_number": "+380995399849",
                                    "skype": "skype", "email": "yulia-knubisoft@octopuslabs.com",
                                    "job_title": "Python Developer"}}]

        self.assertListEqual(actual, expected)

    def test_wrong_system(self):
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id=10,
                                            from_path="$.user.profile.skype",
                                            to_field_name="skype",
                                            active=1, create_dttm=datetime.datetime.now())
        actual = GetInternalModel(1, model.ActiveDirectoryUser.find(email="yulia-knubisoft@octopuslabs.com")[0][
            "active_directory_user_id"]).get_model(self.map)
        expected = [{"system_id": "1",
                     "dictionary": {"last_name": "Probachai", "city": "Vinnitsya", "first_name": "Julia",
                                    "post_code": "21000", "display_name": "Yuliya Probachai",
                                    "updated_at": "2018-05-07T08:18:23+00:00", "home_page": "vk.com",
                                    "country": "Ukraine", "company": "Imagination",
                                    "mobile_phone_number": "+380995399849", "fax": "", "desk_number": "Ukraine",
                                    "work_phone_number": "+380672112999",
                                    "ad_path": "CN=Yuliya Probachai,OU=Test-Users,DC=test-octopus,DC=local",
                                    "manager": "", "street": "Litvinenko", "team": "", "middle_name": "blah",
                                    "login": "Yuliya.Probachai", "job_title": ""}}, {"system_id": "3",
                                                                                     "dictionary": {
                                                                                         "first_name": "Julia",
                                                                                         "last_name": "Probachai",
                                                                                         "middle_name": "",
                                                                                         "description": None,
                                                                                         "end_date": None,
                                                                                         "title": "XXX",
                                                                                         "updated_at": "2018-01-19T00:00:00",
                                                                                         "work_phone_number": "+380672112999",
                                                                                         "mobile_phone_number": "+380995399849",
                                                                                         "manager": None,
                                                                                         "person_number": 1,
                                                                                         "team": None,
                                                                                         "salutation": "Nkpm Tpoegk",
                                                                                         "email": "yulia-knubisoft@octopuslabs.com",
                                                                                         "job_title": None}},
                    {"system_id": "2",
                     "dictionary": {"status": "", "what_do": "Python Developer", "first_name": "Julia",
                                    "last_name": "Probachai", "display_name": "Julia Probachai",
                                    "photo": "https://avatars.slack-edge.com/2018-03-16/331289011283_b33239e4cb8e4d62ae6c_192.jpg",
                                    "updated_at": "2018-05-07T14:06:26+00:00", "linked_in": "http://www.example.com",
                                    "work_phone_number": "+380672112999", "mobile_phone_number": "+380995399849",
                                    "skype": "skype", "email": "yulia-knubisoft@octopuslabs.com",
                                    "job_title": "Python Developer"}}]

        self.assertListEqual(actual, expected)

    def test_not_active_field(self):
        model.FieldReadConfiguration.insert(field_read_configuration_id=uuid.uuid4().hex, system_id=2,
                                            from_path="$.user.profile.skype",
                                            to_field_name="skype",
                                            active=0, create_dttm=datetime.datetime.now())
        actual = GetInternalModel(1, model.ActiveDirectoryUser.find(email="yulia-knubisoft@octopuslabs.com")[0][
            "active_directory_user_id"]).get_model(self.map)
        expected = [{"system_id": "1",
                     "dictionary": {"last_name": "Probachai", "city": "Vinnitsya", "first_name": "Julia",
                                    "post_code": "21000", "display_name": "Yuliya Probachai",
                                    "updated_at": "2018-05-07T08:18:23+00:00", "home_page": "vk.com",
                                    "country": "Ukraine", "company": "Imagination",
                                    "mobile_phone_number": "+380995399849", "fax": "", "desk_number": "Ukraine",
                                    "work_phone_number": "+380672112999",
                                    "ad_path": "CN=Yuliya Probachai,OU=Test-Users,DC=test-octopus,DC=local",
                                    "manager": "", "street": "Litvinenko", "team": "", "middle_name": "blah",
                                    "login": "Yuliya.Probachai", "job_title": ""}}, {"system_id": "3",
                                                                                     "dictionary": {
                                                                                         "first_name": "Julia",
                                                                                         "last_name": "Probachai",
                                                                                         "middle_name": "",
                                                                                         "description": None,
                                                                                         "end_date": None,
                                                                                         "title": "XXX",
                                                                                         "updated_at": "2018-01-19T00:00:00",
                                                                                         "work_phone_number": "+380672112999",
                                                                                         "mobile_phone_number": "+380995399849",
                                                                                         "manager": None,
                                                                                         "person_number": 1,
                                                                                         "team": None,
                                                                                         "salutation": "Nkpm Tpoegk",
                                                                                         "email": "yulia-knubisoft@octopuslabs.com",
                                                                                         "job_title": None}},
                    {"system_id": "2",
                     "dictionary": {"status": "", "what_do": "Python Developer", "first_name": "Julia",
                                    "last_name": "Probachai", "display_name": "Julia Probachai",
                                    "photo": "https://avatars.slack-edge.com/2018-03-16/331289011283_b33239e4cb8e4d62ae6c_192.jpg",
                                    "updated_at": "2018-05-07T14:06:26+00:00", "linked_in": "http://www.example.com",
                                    "work_phone_number": "+380672112999", "mobile_phone_number": "+380995399849",
                                    "skype": "skype", "email": "yulia-knubisoft@octopuslabs.com",
                                    "job_title": "Python Developer"}}]
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
