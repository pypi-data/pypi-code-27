from components.merging import MergeProcess
from tests.merge_data import *
from tests.parent import BaseTestCase


class TestMerge(BaseTestCase):
    default = {"system_id": 1,
               "dictionary": {"first_name": "Name1", "last_name": "LastName1", "login": "", "email": "Email1",
                              "age": 20,
                              "updated_at": "2018-01-18 12:00:00.000000"}}

    # empty fields what was empty in default data shoudn't be in merge
    def test_change_field(self):
        output = MergeProcess(1, "").merge([self.default, a1, a2, a3, a4, a5])
        expected = {"first_name": "Name2", "last_name": "LastName2", "age": 21,
                    "updated_at": "2018-01-18 15:00:00.000000", "email": "Email2"}
        self.assertDictEqual(output, expected)

    def test_add_custom_filed(self):
        output = MergeProcess(2, "").merge([self.default, c1, c2, c3, c4, c5])
        expected = {"first_name": "Name2", "last_name": "LastName1", "custom_filed_2": "abc", "login": "Login1",
                    "age": 21, "updated_at": "2018-01-18 15:00:00.000000", "email": "Email2"}
        self.assertDictEqual(output, expected)


    def test_big_merge(self):
        output = MergeProcess(3, "").merge([self.default, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10])
        expected = {"custom_filed_1": "abc", "first_name": "Name2", "last_name": "LastName2", "photo": "some_photo1",
                    "title": "MR", "login": "", "age": 21, "updated_at": "2018-01-18 22:28:04.551000",
                    "custom_filed_2": "abc", "email": "Email2"}
        self.assertDictEqual(output, expected)

    def test_no_changes(self):
        output = MergeProcess(4, "").merge([self.default, d1, d2, d3])
        expected = {"first_name": "Name1", "last_name": "LastName1", "login": "Login1", "age": 20,
                    "updated_at": "2018-01-18 14:00:00.000000", "email": "Email1"}
        self.assertDictEqual(output, expected)

    #when there aren't any updates merge should return default data
    def test_old_date(self):
        output = MergeProcess(5, "").merge([self.default, e1, e2, e3])
        expected = {"first_name": "Name1", "last_name": "LastName1", "login": "", "email": "Email1",
                    "age": 20,
                    "updated_at": "2018-01-18 12:00:00.000000"}
        self.assertDictEqual(output, expected)
