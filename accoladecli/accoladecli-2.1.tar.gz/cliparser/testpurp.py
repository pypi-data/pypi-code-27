# !/usr/bin/env python3
# chmod +x "file name"
import getpass
import json
import hashlib
import requests
import argparse
import boto3
import os
import botocore

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

accolade_group = subparser.add_parser('storage')
accolade_subparser2 = accolade_group.add_subparsers()

accolade_remove = accolade_subparser2.add_parser('remove')
accolade_remove.set_defaults(which='remove')
#accolade_remove.add_argument('rbucket', help="Bucket of object to be removed")
accolade_remove.add_argument('rkey', help="Key within bucket to remove file")

accolade_upload = accolade_subparser2.add_parser('upload')
accolade_upload.set_defaults(which='upload')
accolade_upload.add_argument('file', help="File that will be upload into the bucket-key location")
#accolade_upload.add_argument('bucket', help="Bucket that the file will be uploaded to")
#accolade_upload.add_argument('key', help="Key that the file will be uploaded to")
accolade_upload.add_argument('--replace', help="Include on command line if replacing another file", action='store_true')

accolade_dirupload = accolade_subparser2.add_parser('dirupload')
accolade_dirupload.set_defaults(which='dirupload')
accolade_dirupload.add_argument('directory', help="Absolute path to the directory that will be copied")
accolade_dirupload.add_argument('bucketname', help="Bucket that files will be uploaded too")
accolade_dirupload.add_argument('key', help="Key that files will be uploaded to")


args = vars(parser.parse_args())

which = args['which']

session = boto3.Session(profile_name='test')
s3res = session.resource('s3')
s3client = session.client('s3')


def uploadDirectory(path, bucketname, key):
    for root, dirs, files in os.walk(path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, path)
            s3_path = os.path.join(key, relative_path)
            if file != '.DS_Store':
                s3client.upload_file(local_path, bucketname, s3_path)



#Resource owner's credentials
username = input('Username: ' )
password = getpass.getpass('Passcode: ')
print(username)
print(password)


def hashfunc(input):
    return hashlib.sha256('{}'.format(input).encode('utf-8')).hexdigest()


# Storing data dictionary as a parameter for the Accolade token below
data = {'grant_type': 'password', 'username': username, 'password': password}

username = hashfunc(username)

try:
    upaddon = '/' + args['file'].split('/')[-1]
except:
    upaddon = '/' + args['rkey'].split('/')[-1]


#One-way SSL(just server is certifie), Two-way SSL(both must have certifications), or some API gateway to have logging is necessary


# For key, must put location/file name
if which == 'upload':
    if args['replace']:
        try:
            s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + upaddon).load()
            print("going to replace now!")
            s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username).delete()
            s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548','Hashed/' + username + upaddon)
        except botocore.exceptions.ClientError:
            # For now pretending that accolade-platform-ext-dev-partners-577121982548 is makeup bucket
            print("Going into makeup bucket")
            s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + upaddon)
    else:
        s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + upaddon)




elif which == 'dirupload':
    uploadDirectory(args['directory'], args['bucketname'], args['key'])


elif which == 'remove':
    s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + upaddon).delete()


token_url = "https://login-test3.myaccolade.com/token"



print('\n')


#client's credentials
client_id = 'etp-admin'
client_secret = 'AJ8t1jknpgd2flqM2-JAs3cIi3EV3Y02jk_WPeMl1LfGRSbZyoIiXx50rCPYbfHKTNgXDTOaE0xCpMwZpexbmIY'

# Single call with resource owner credentials in variable "data" and then client credentials in the "auth"
# Should return the access_token



# May have to include if not working:verify=False,
access_token_response = requests.post(token_url, data=data, allow_redirects=False, auth=(client_id, client_secret))

print("Lets now print the type of the access_token_response:")
print(type(access_token_response))
print('\n')
print("Here are the headers of the access_token_response:")
print(access_token_response.headers)
print('\n')
print("Now printing the type of the headers:")
print(type(access_token_response.headers))
print('\n')

print("Here are the text of the access_token_reponse:")
print(access_token_response.text)
print('\n')

tokens = json.loads(access_token_response.text)
print("let's now print the type of the tokens:")
print(type(tokens))
print('\n')
print("I am now printing the access token: " + "\n" + tokens['access_token'])
print('\n')
print("I am now printing the id token: " + "\n" + tokens['id_token'])


client = boto3.client('sts')



token = "eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZDg5M2I2Yy04YTYzLTRmNTgtOTAxYi01ZDA0YWU4NzExZmUiLCJhdWQiOiJldHAtYWRtaW4iLCJraWQiOiJyc2ExIiwiaXNzIjoiaHR0cHM6XC9cL2xvZ2luLXRlc3QzLm15YWNjb2xhZGUuY29tXC8iLCJleHAiOjE1MzE3NjM4MDIsImlhdCI6MTUzMTc2MzIwMiwianRpIjoiMzRiYjRiYjAtM2UyZS00YThjLTlhYjItNzg1MDgzMDFjODNkIn0.QykzGp7u87Y0JQS6Fl0TUCbF-N73LXXnFNLdD6xpDL4T4M58P7KeQ9OkYCw9xlBhwk3JzfhQ8Iqf__eU0NFql97UyGHi3eCQ-zNuQVya1UdidL1tBpTCJZrEzYhzHmNM2BWd7Mlb1pwSj_qyaoOTrx-POyik25NoH5VBM4XXLqehkQK3sBWN-vSPPEJZgFWzfraCtKrrnzoI9Sxx5tuxsd2ABD91quLfwsBkbxdW3ax56QMz8CF3D42RqxvDi388-SQA7JphLhoIS7dlGz3cQRXv8MkyeXptGvVFtdu2QgGAUoGL3_oJpmkrsKMdJKvcRKBa2AbiG-KuzqqyYTImkw"


uh = hashfunc('UnitedHealth')
at = hashfunc('Aetna')
ks = hashfunc('Kaiser')
ws = hashfunc('Wellpoint')

username = hashfunc(username)



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
                   #"aws:SourceIp": ["72.309.38.2/32", "Insert more IP's here in list format"]

               }
           }
       },
       {
      "Sid": "KeyAllow",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::examplebucket/" + uh, "arn:aws:s3:::examplebucket/" + at, "arn:aws:s3:::examplebucket/" + ks,
             "arn:aws:s3:::examplebucket/" + ws],
       }
   ]
}

#Accolade's IP Address- 50.251.254.133
#username, date, file being removed, action being taken

# policyrestr = json.dumps(jsonrestr)
#
#
# assumed_role_object = client.assume_role_with_web_identity(
#    # RoleArn="arn:aws:iam::ACCOUNT-ID-WITHOUT-HYPHENS:role/ROLE-NAME",
#     RoleArn="arn:aws:iam::vikramchandran:role/user-pegasus",
#     RoleSessionName="practicesession", WebIdentityToken=token)
#
#
#
# accesskey = assumed_role_object['Credentials']['AccessKeyId']
# secretaccesskey = assumed_role_object['Credentials']['SecretAccessKey']
# sessiontoken = assumed_role_object['Credentials']['SessionToken']
#
# print("Credentials are: " + "\n")
# print("AccessKey Id: %s" % accesskey)
# print("SecretAccessKey: %s" % secretaccesskey)
# print("SessionToken: %s" % sessiontoken)
#
# session = boto3.Session(profile_name='test', aws_access_key_id=accesskey, aws_secret_access_key=secretaccesskey, aws_session_token=sessiontoken)

# Then add all the master code as below