import unittest

import boto3
from moto import mock_s3

from external_data_structures.dictionaries.s3 import S3Dict



class TestS3Dict(unittest.TestCase):

  @mock_s3
  def setUp(self):
    self.bucket = S3Dict('test-4e1243')
    self.bucket.s3.create_bucket(Bucket='test-4e1243')

  
  def test_s3_dict_int_assignment_and_retrieval(self):
    self.bucket['asd'] = 123
    self.assertEqual(123, self.bucket['asd'])

  def test_s3_dict_str_assignment_and_retrieval(self):
    self.bucket['msg'] = "hello world"
    self.assertEqual("hello world", self.bucket['msg'])

  def test_s3_dict_list_assignment_and_retrieval(self):
    self.bucket['msg'] = [1,2, 3, "a", "b", "c"]
    self.assertEqual([1,2, 3, "a", "b", "c"], self.bucket['msg'])

  def test_s3_dict_dict_assignment_and_retrieval(self):
    self.bucket['msg'] = {"a": None, "b": 2, "c" : "c"}
    self.assertEqual({"a": None, "b": 2, "c" : "c"}, self.bucket['msg'])


if __name__ == '__main__':
    unittest.main()