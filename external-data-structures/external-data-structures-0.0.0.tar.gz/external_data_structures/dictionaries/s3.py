from functools import wraps

import boto3
import botocore

from .prototype import ProtoTypeDict
from recursive_itertools import rfilter
from generic_encoders import ComposedEncoder, JsonEncoder, GzipEncoder, TextEncoder


def convert_s3_http_errors(func):
    @wraps(func)
    def convert_s3_http_errors_h(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except botocore.exceptions.ClientError as e:
        if e.response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 404:
          raise KeyError(key)
        else:
          raise e
    return convert_s3_http_errors_h


default_key_serializer = TextEncoder().inverted
default_object_serializer = ComposedEncoder(JsonEncoder(), TextEncoder(), GzipEncoder())


class S3Dict(ProtoTypeDict):

  def __init__(self, bucket, prefix='', key_serializer=default_key_serializer, serializer=default_object_serializer):
    self.bucket_name = bucket
    self.prefix = prefix
    self.s3 = boto3.resource('s3')
    self.bucket = self.s3.Bucket(bucket)

    super(S3Dict, self).__init__(
      prefix=prefix,
      key_serializer=key_serializer,
      serializer=serializer)

  def make_key(self, key):
    return "{}{}".format(self.prefix, self.key_serializer.encode(key))

  def get_object_handle(self, key):
    return self.bucket.Object(self.make_key(key))

  @convert_s3_http_errors
  def get_object_stream(self, key):
    try:
      return self.get_object_handle(key).get()['Body']
    except botocore.exceptions.ClientError as e:
      if e.response.get('ResponseMetadata', {}).get('HTTPStatusCode', None) == 404:
        raise KeyError(key)
      else:
        raise e

  def __getitem__(self, key):
    return self.serializer.decode(self.get_object_stream(key).read())

  def __setitem__(self, key, value):
    return self.put_object(key, value)

  @convert_s3_http_errors
  def __contains__(self, key):
    try:
      self.get_object_handle(key).load()
    except KeyError:
      return False
    return True

  @convert_s3_http_errors
  def __delitem__(self, key):
    self.get_object_handle(key).load()

  def put_object(self, key, value, ContentType=None, ContentEncoding=None):
    value = self.serializer.encode(value)
    args = {
      'Body': value,
      'ContentType': ContentType,
      'ContentEncoding': ContentEncoding
    }
    self.get_object_handle(key).put(
      **rfilter(args, lambda x: x is not None)
      )

  def iterkeys(self):
    for obj in self.bucket.objects.filter(Prefix=self.prefix):
      key = self._strip_key_prefix_and_decode(obj.key)
      yield key
