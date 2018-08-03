import json
import unittest
from datetime import datetime

import pytz
from tornado.options import options

import model
import utils
from components.providers import Slack, ActiveDirectory, SelectHR
from tests.parent import BaseTestCase


class TestGetJson(BaseTestCase):

    def test_slack1(self):
        # user exists in AD and Slack

        output = Slack("1").get_json(self.user)

        def get_additional_fields(user_id):
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"token": options.slack_api_token, "user": user_id}
            result = utils.make_request(options.slack_api_url, "users.profile.get", data, headers, "POST",
                                        json_type=False, json_response=True)

            return result["profile"] if result["ok"] else {}

        def download_raw_data_per_user(user):
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"token": options.slack_api_token, "email": user["email"]}
            result = utils.make_request(options.slack_api_url, "users.lookupByEmail", data, headers, "POST",
                                        json_type=False, json_response=True)
            if not result["ok"]:
                raise RuntimeError("Slack user is not found")

            id = result.get("user")["id"]
            if id:
                result["user"]["profile"].update(get_additional_fields(id))

            return result

        def __transform__(data, user):
            date = data["user"]["updated"]
            data["user"]["updated"] = pytz.UTC.localize(datetime.fromtimestamp(date)).isoformat()
            try:
                manager_id = data["user"]["profile"]["fields"]["Xf9QCRHNM9"]
                manager = get_additional_fields(manager_id["value"])["real_name"]
                manager_id["value"] = manager
                return data
            except Exception as e:
                return data

        expected = __transform__(download_raw_data_per_user(self.user), self.user)
        self.assertDictEqual(output, expected)

    def test_slack2(self):
        # user exists in AD and not exists in Slack
        output = Slack("1").get_json(model.ActiveDirectoryUser.find(email="jake.caulton@octopusinvestments.com")[0])
        expected = None
        self.assertEqual(output, expected)

    def test_slack3(self):
        # user doesn"t have email
        user_id = model.ActiveDirectoryUser.add_active_directory_user("Blah", "Blah", "some_login", "",
                                                                      "{'Some': 'awesome'}")
        user = model.ActiveDirectoryUser.find(active_directory_user_id=user_id)[0]
        output = Slack("1").get_json(user)
        expected = None
        self.assertEqual(output, expected)

    def test_ad1(self):
        output = ActiveDirectory("1").get_json(self.user)
        expected = ActiveDirectory("1").__transform__(json.loads(self.user["metadata"]), self.user)

        self.assertDictEqual(output, expected)

    def test_hr(self):
        output = SelectHR("1").get_json(self.user)
        expected = {"biography": None,
                    "birth_date": datetime(1981, 1, 1, 0, 0),
                    "date_purged": None,
                    "e-mail": "yulia-knubisoft@octopuslabs.com",
                    "end_date": None,
                    "first_name": "Julia",
                    "formal_name": "Haivlf Mxsnet",
                    "gender": "Unknown",
                    "initials": "",
                    "manager_name": None,
                    "mobile_phone_number": "+380995399849",
                    "nationality": None,
                    "person_notes": None,
                    "person_number": 1,
                    "post_name": None,
                    "post_number": None,
                    "salutation": "Nkpm Tpoegk",
                    "second_name": "",
                    "start_date": None,
                    "surname": "Probachai",
                    "title": "XXX",
                    "unit_name": None,
                    "updated_at": "2018-01-19T00:00:00",
                    "work_mobile_phone_number": None,
                    "work_phone_number": "+380672112999"}
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
