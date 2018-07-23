import urllib, json
import hashlib
import boto3



client = boto3.client('sts')

def hashfunc(input):
    return hashlib.sha256('{}'.format(input).encode('utf-8')).hexdigest()


token = "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZDg5M2I2Yy04YTYzLTRmNTgtOTAxYi01ZDA0YWU4NzExZmUiLCJhdWQiOiJldHAtYWRtaW4iLCJraWQiOiJyc2ExIiwiaXNzIjoiaHR0cHM6XC9cL2xvZ2luLXRlc3QzLm15YWNjb2xhZGUuY29tXC8iLCJleHAiOjE1MzE3NjM4MDIsImlhdCI6MTUzMTc2MzIwMiwianRpIjoiMzRiYjRiYjAtM2UyZS00YThjLTlhYjItNzg1MDgzMDFjODNkIn0.QykzGp7u87Y0JQS6Fl0TUCbF-N73LXXnFNLdD6xpDL4T4M58P7KeQ9OkYCw9xlBhwk3JzfhQ8Iqf__eU0NFql97UyGHi3eCQ-zNuQVya1UdidL1tBpTCJZrEzYhzHmNM2BWd7Mlb1pwSj_qyaoOTrx-POyik25NoH5VBM4XXLqehkQK3sBWN-vSPPEJZgFWzfraCtKrrnzoI9Sxx5tuxsd2ABD91quLfwsBkbxdW3ax56QMz8CF3D42RqxvDi388-SQA7JphLhoIS7dlGz3cQRXv8MkyeXptGvVFtdu2QgGAUoGL3_oJpmkrsKMdJKvcRKBa2AbiG-KuzqqyYTImkw"


uh = hashfunc('UnitedHealth')
at = hashfunc('Aetna')
ks = hashfunc('Kaiser')
ws = hashfunc('Wellpoint')



jsonrestr = {
   "Id": "S3PolicyRestrictions",
   "Statement": [
       {
           "Sid": "IPDeny",
           "Effect": "Deny",
           "Principal": {
               "AWS": "*"
           },
           "Action": "s3:*",
           "Resource": "*",
           "Condition": {
               "NotIpAddress": {
                   "aws:SourceIp": "72.309.38.2/32"
                   # "aws:SourceIp": ["72.309.38.2/32", "Insert more IP's here in list format"]

               }
           }
       },
       {
      "Sid": "IPAllow",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::examplebucket/uh", "arn:aws:s3:::examplebucket/at", "arn:aws:s3:::examplebucket/ks",
             "arn:aws:s3:::examplebucket/ws"],
       }
   ]
}

policyrestr = json.dumps(jsonrestr)


assumed_role_object = client.assume_role_with_web_identity(
   # RoleArn="arn:aws:iam::ACCOUNT-ID-WITHOUT-HYPHENS:role/ROLE-NAME",
    RoleArn="arn:aws:iam::vikramchandran:role/user-pegasus",
    RoleSessionName="practicesession", WebIdentityToken=token)



accesskey = assumed_role_object['Credentials']['AccessKeyId']
secretaccesskey = assumed_role_object['Credentials']['SecretAccessKey']
sessiontoken = assumed_role_object['Credentials']['SessionToken']

print("Credentials are: " + "\n")
print("AccessKey Id: %s" % accesskey)
print("SecretAccessKey: %s" % secretaccesskey)
print("SessionToken: %s" % sessiontoken)

session = boto3.Session(profile_name='test', aws_access_key_id=accesskey, aws_secret_access_key=secretaccesskey, aws_session_token=sessiontoken)

# Then add all the master code as below


def url_conversion(assumed_role_object):
    # Converting to JSON format
    json_string_with_temp_credentials = '{'
    json_string_with_temp_credentials += '"sessionId":"' + assumed_role_object['Credentials']['AccessKeyId'] + '",'
    json_string_with_temp_credentials += '"sessionKey":"' + assumed_role_object['Credentials']['SecretAccessKey'] + '",'
    json_string_with_temp_credentials += '"sessionToken":"' + assumed_role_object['Credentials']['SessionToken'] + '"'
    json_string_with_temp_credentials += '}'

    request_parameters = "?Action=getSigninToken"
    request_parameters += "&SessionDuration=43200"
    request_parameters += "&Session=" + urllib.quote_plus(json_string_with_temp_credentials)
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    r = requests.get(request_url)

    # Returns a JSON document with a single element named SigninToken.
    signin_token = json.loads(r.text)

    request_parameters = "?Action=login"
    request_parameters += "&Issuer=Example.org"
    request_parameters += "&Destination=" + urllib.quote_plus("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token["SigninToken"]
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    return request_url

# This in the bottom for other ways to restrict IP addresses

# {
#   "Version": "2012-10-17",
#   "Id": "S3PolicyId1",
#   "Statement": [
#     {
#       "Sid": "IPAllow",
#       "Effect": "Allow",
#       "Principal": "*",
#       "Action": "s3:*",
#       "Resource": "arn:aws:s3:::examplebucket/*",
#       "Condition": {
#          "IpAddress": {"aws:SourceIp": "54.240.143.0/24"},
#          "NotIpAddress": {"aws:SourceIp": "54.240.143.188/32"}
#       }
#     }
#   ]
# }


