'''
  File Name: s3Helper.py
  Author: Daniel Fritsch
  Date created: May 4 2018
  Python Version: 3.6
'''
import boto3
import math
import json
import io

RESOURCE = boto3.resource('s3')
CLIENT = boto3.client('s3')

JSON = "json"
STR = "str"

def download_file(bucket, key, local_path):
    """
    Grab a file from S3 and bring it onto your local machine at the
    specified path.

    bucket (str)     -- Bucket that the file exists in
    key (str)        -- Key that the file exists in
    local_path (str) -- Where the file will be stored on the caller's machine
    """
    RESOURCE.Bucket(bucket).download_file(key, local_path)

def extract_file_content(bucket, key):
    """
    Take the contents from a JSON file in S3 and convert them into a dictionary
    on the caller's machine. Similar to download, but without bringing the file
    onto the user's machine. 

    bucket (str) -- Bucket that the file exists in
    key (str)    -- Key that the file exists in
    """
    response = CLIENT.get_object(
        Bucket = bucket,
        Key = key
    )
    jsonContent = json.loads(response['Body'].read())
    return jsonContent

def extract_file_content_with_type(bucket, key, ret_type):
    """
    Similar to extract_file_content, but in this func you may specify the way you
    want the file content to be returned.

    bucket (str)  -- Bucket that the file exists in
    key (str)     -- Key that the file exists in
    ret_type(str) -- Either "json" or "str" to specify what return type is desired.
    """
    response = CLIENT.get_object(
        Bucket = bucket,
        Key = key
    )
    is_json = lambda c: c == JSON
    if is_json(ret_type):
        return json.loads(response['Body'].read())

    is_str = lambda c: c == STR
    if is_str(ret_type):
        return response['Body'].read().decode("utf-8")

def export_content_to_file(bucket, key, content):
    """
    Store the contents of a dictionary in a S3 JSON file. 

    bucket (str)   -- Bucket that the file exists in
    key (str)      -- Key that the file exists in
    contents (dict) -- the content to store as a JSON file in S3
    """
    response = CLIENT.put_object(
        Body = json.dumps(content, indent=4),
        Bucket = bucket,
        Key = key
    )

def get_s3_keys(bucket, prefix):
    """
    Get a list of keys in an S3 bucket.

    bucket -- Bucket that the file exits in.
    prefix -- The rest of the path for the desired directory. This will limit
              the results to be only the keys in 'bucket' that begin with this
              prefix. Use an empty str '' for this param if all keys are desired
    """
    keys = []
    resp = CLIENT.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if resp['KeyCount'] == 0:
        return keys
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys

def get_last_modified_time(bucket, key):
    """
    Returns the 'Last Modified' time of the specified file in UTC timezone.
    
    bucket (str)   -- Bucket that the file exists in
    key (str)      -- Key that the file exists in
    """
    response = CLIENT.head_object(
        Bucket=bucket, 
        Key=key
    )
    return response['LastModified']


def main():
    pass

if __name__ == "__main__":
    main()
