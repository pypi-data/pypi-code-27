# Copyright 2018 S,artronix Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#!/usr/bin/python

import sys
import boto.sts
import boto.s3
import boto3
import requests
import getpass
import ConfigParser
import base64
import logging
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
from os.path import expanduser
from urlparse import urlparse, urlunparse

import requests
import argparse
import json
import jmespath
import os


__version__ = '0.1.0'
name = "smxsso"


##########################################################################
# Variables

# region: The default AWS region that this script will connect
# to for all API calls
region = 'us-east-1'

# output format: The AWS CLI output format that will be configured in the
# saml profile (affects subsequent CLI calls)
outputformat = 'json'

# awsconfigfile: The file where this script will store the temp
# store credentials under the saml profile
awsconfigfile = '/.aws/credentials'

# SSL certificate verification: Whether or not strict certificate
# verification is done, False should only be used for dev/test
sslverification = True

# idpentryurl: The initial url that starts the authentication process.
idpentryurl = 'https://sso.cloudassured.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices' 

# Uncomment to enable low level debugging
# logging.basicConfig(level=logging.DEBUG)

# MFA Verification Option choice
# verificationOption0 = mobile app
# verificationOption1 = phone call
# verificationOption2 = sms
verificationOption = 'verificationOption0'
url = os.environ.get('accounts_url','https://s3.amazonaws.com/camsdev-automation/CloudCheckr/Accounts.json')

s3 = boto3.client('s3')
s3_bucket= 'camsdev-automation'
s3_object_key = 'CloudCheckr/Accounts.json'

##########################################################################

def login(profile):
    # Get the federated credentials from the user
    print "Username:",
    username = raw_input()
    password = getpass.getpass()
    print ''

    # Initiate session handler
    session = requests.Session()

    # Programmatically get the SAML assertion
    # Opens the initial IdP url and follows all of the HTTP302 redirects, and
    # gets the resulting login page
    formresponse = session.get(idpentryurl, verify=sslverification)
    # Debug the formresponse if needed
    #print formresponse.text
    # Capture the idpauthformsubmiturl, which is the final url after all the 302s
    idpauthformsubmiturl = formresponse.url

    # Parse the response and extract all the necessary values
    # in order to build a dictionary of all of the form values the IdP expects
    formsoup = BeautifulSoup(formresponse.text.decode('utf8'),"lxml")
    payload = {}

    for inputtag in formsoup.find_all(re.compile('(INPUT|input)')):
        name = inputtag.get('name','')
        value = inputtag.get('value','')
        if "user" in name.lower():
            #Make an educated guess that this is the right field for the username
            payload[name] = username
        elif "email" in name.lower():
            #Some IdPs also label the username field as 'email'
            payload[name] = username
        elif "pass" in name.lower():
            #Make an educated guess that this is the right field for the password
            payload[name] = password
        else:
            #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
            payload[name] = value

    # Set our AuthMethod to Form-based auth because the code above sees two values
    # for authMethod and the last one is wrong
    payload['AuthMethod'] = 'FormsAuthentication'

    # Debug the parameter payload if needed
    # Use with caution since this will print sensitive output to the screen

    # print payload

    # Some IdPs don't explicitly set a form action, but if one is set we should
    # build the idpauthformsubmiturl by combining the scheme and hostname 
    # from the entry url with the form action target
    # If the action tag doesn't exist, we just stick with the 
    # idpauthformsubmiturl above
    for inputtag in formsoup.find_all(re.compile('(FORM|form)')):
        action = inputtag.get('action')
        loginid = inputtag.get('id')
        if (action and loginid == "loginForm"):
            parsedurl = urlparse(idpentryurl)
            idpauthformsubmiturl = parsedurl.scheme + "://" + parsedurl.netloc + action

    # print idpauthformsubmiturl
    # print ''

    # Performs the submission of the IdP login form with the above post data
    loginresponse = session.post(
        idpauthformsubmiturl, data=payload, verify=sslverification)

    # Debug the response if needed
    # print (loginresponse.text)

    # MFA Step 1 - If you have MFA Enabled, there are two additional steps to authenticate
    # Choose a verification option and reload the page

    # Capture the idpauthformsubmiturl, which is the final url after all the 302s
    mfaurl = loginresponse.url

    loginsoup = BeautifulSoup(loginresponse.text.decode('utf8'),"lxml")
    payload2 = {}

    for inputtag in loginsoup.find_all(re.compile('(INPUT|input)')):
        name = inputtag.get('name','')
        value = inputtag.get('value','')
        #Simply populate the parameter with the existing value (picks up hidden fields in the login form)
        payload2[name] = value

    # Set mfa auth type here...
    payload2['__EVENTTARGET'] = verificationOption
    payload2['AuthMethod'] = 'TOTPAuthenticationProvider-New'
    print "Enter MFA 6-digit Code:",
    payload2['ChallengeQuestionAnswer'] = raw_input()

    mfaresponse = session.post(
        mfaurl, data=payload2, verify=sslverification)

    # if mfaresponse.history:
    #     print "Request was redirected"
    #     for resp in mfaresponse.history:
    #         print resp.status_code, resp.url
    #     print "Final destination:"
    #     print mfaresponse.status_code, mfaresponse.url
    # else:
    #     print "Request was not redirected"
    # # Debug the response if needed
    # #print ('MF:'+mfaresponse.text)

    # # Debug the response if needed
    # print(mfaresponse.cookies.get_dict())
    # for r in mfaresponse.cookies:
        
    #     print('\n')
    #     print (base64.b64decode(r.value))
    #     print('Non-Standard\n')
    #     print (r.get_nonstandard_attr)

    # MFA Step 2 - Fire the form and wait for verification

    # # Decode the response and extract the SAML assertion
    soup = BeautifulSoup(mfaresponse.text.decode('utf8'),'lxml')
    assertion = ''

    # Look for the SAMLResponse attribute of the input tag (determined by
    # analyzing the debug print lines above)
    for inputtag in soup.find_all('input'):
        if(inputtag.get('name') == 'SAMLResponse'):
            # (inputtag.get('value'))
            assertion = inputtag.get('value')

    # Better error handling is required for production use.
    if (assertion == ''):
        #TODO: Insert valid error checking/handling
        print 'Response did not contain a valid SAML assertion'
        sys.exit(0)

    # Debug only
    # print(base64.b64decode(assertion))

    # Parse the returned assertion and extract the authorized roles
    awsroles = []
    root = ET.fromstring(base64.b64decode(assertion))
    for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
        if (saml2attribute.get('Name') == 'https://aws.amazon.com/SAML/Attributes/Role'):
            for saml2attributevalue in saml2attribute.iter('{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'):
                awsroles.append(saml2attributevalue.text)

    # Note the format of the attribute value should be role_arn,principal_arn
    # but lots of blogs list it as principal_arn,role_arn so let's reverse
    # them if needed
    for awsrole in awsroles:
        chunks = awsrole.split(',')
        if'saml-provider' in chunks[0]:
            newawsrole = chunks[1] + ',' + chunks[0]
            index = awsroles.index(awsrole)
            awsroles.insert(index, newawsrole)
            awsroles.remove(awsrole)

    # lookup Account vanity names from CC sync file
    
    json_data = None
    try:
        #s3_response = s3.get_object(Bucket=s3_bucket, Key=s3_object_key)
        #json_data = json.load(s3_response['Body'])
        response = requests.get(url)
        json_data = json.loads(response.text)
    except:
        print 'Unable to retreive CC Accounts.'
        json_data = None
    #print(json_data)
    
    # If I have more than one role, ask the user which one they want,
    # otherwise just proceed
    print ""
    if len(awsroles) > 1:
        i = 0
        print "Please choose the role you would like to assume:"
        for awsrole in awsroles:
            if json_data != None:
                accountId = awsrole.split(',')[0].split(':')[4]
                #print accountId
                accountName = jmespath.search("Accounts[?aws_account_id=='{}'].account_name".format(accountId),json_data)
                #print accountName
                if accountName:
                    print '[', i, ']: ', accountName[0]+' ('+ awsrole.split(',')[0]+')'
                else:
                    print '[', i, ']: ', awsrole.split(',')[0]
            else:
                print '[', i, ']: ', awsrole.split(',')[0]
            i += 1
        print "Selection: ",
        selectedroleindex = raw_input()

        # Basic sanity check of input
        if int(selectedroleindex) > (len(awsroles) - 1):
            print 'You selected an invalid role index, please try again'
            sys.exit(0)

        role_arn = awsroles[int(selectedroleindex)].split(',')[0]
        principal_arn = awsroles[int(selectedroleindex)].split(',')[1]
    else:
        role_arn = awsroles[0].split(',')[0]
        principal_arn = awsroles[0].split(',')[1]

    # Use the assertion to get an AWS STS token using Assume Role with SAML
    conn = boto.sts.connect_to_region(region)
    token = conn.assume_role_with_saml(role_arn, principal_arn, assertion)

    # Write the AWS STS token into the AWS credential file
    home = expanduser("~")
    filename = home + awsconfigfile

    # Read in the existing config file
    config = ConfigParser.RawConfigParser()
    config.read(filename)

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if not config.has_section(profile):
        config.add_section(profile)

    config.set(profile, 'output', outputformat)
    config.set(profile, 'region', region)
    config.set(profile, 'aws_access_key_id', token.credentials.access_key)
    config.set(profile, 'aws_secret_access_key', token.credentials.secret_key)
    config.set(profile, 'aws_session_token', token.credentials.session_token)

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write(configfile)

    # Give the user some basic info as to what has just happened
    print '\n\n----------------------------------------------------------------'
    print 'Your new access key pair has been stored in the AWS configuration file "{0}" under the "{1}" profile.'.format(filename, profile)
    print 'Note that it will expire at {0}.'.format(token.credentials.expiration)
    print 'After this time, you may safely rerun this script to refresh your access key pair.'
    print 'To use this credential, call the AWS CLI with the --profile option (e.g. aws --profile {0} ec2 describe-instances).'.format(profile)
    print 'To use other static credentials, call the AWS CLI with the --profile option (e.g. aws --profile <name> ec2 describe-instances).'
    print 'You may also clear out your credentials for your profile by re running this script using the following command (e.g. python ssoadfs.py --action logout --profile {0})'.format(profile)
    print '----------------------------------------------------------------\n\n'

    # Use the AWS STS token to list all of the S3 buckets
    s3conn = boto.s3.connect_to_region(region,
                        aws_access_key_id=token.credentials.access_key,
                        aws_secret_access_key=token.credentials.secret_key,
                        security_token=token.credentials.session_token)

    buckets = s3conn.get_all_buckets()

    print '\nSimple API example listing all S3 buckets: "aws --profile={} s3 ls"'.format(profile)
    print(buckets)
def logout(profile):
    print '\n\n----------------------------------------------------------------'
    print 'Are you sure you want to logout and remove all credentials for the "{}" profile?'.format(profile)
    print 'Press CTRL+C to cancel or press ENTER to contnue.'
    print '----------------------------------------------------------------\n\n'
    raw_input()
    # Write the AWS STS token into the AWS credential file
    home = expanduser("~")
    filename = home + awsconfigfile

    # Read in the existing config file
    config = ConfigParser.RawConfigParser()
    config.read(filename)

    # Put the credentials into a saml specific section instead of clobbering
    # the default credentials
    if config.has_section(profile):
        config.remove_section(profile)

    # Write the updated config file
    with open(filename, 'w+') as configfile:
        config.write(configfile)

    # Give the user some basic info as to what has just happened
    print '\n\n----------------------------------------------------------------'
    print 'Your access keys have been cleared out in the AWS configuration file "{0}" under the "{1}" profile.'.format(filename, profile)
    print '----------------------------------------------------------------\n\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='Action to be taken. Options include "login" or "logout". Defaults to "login" if no action is provided.')
    parser.add_argument('--profile', help='Profile name used to store AWS credentials. Note: Existing profile credentials will be re-written. If no profile name is provided, "default" will be used.')
    args = parser.parse_args()
    print '\n-------------------------------------------------------------------------------------------------------------'
    profile=''
    if (not args.profile):
        # Profile Name used by default
        profile = 'default'
        print 'No profile parameter was supplied. Using "{0}" profile. Note: any existing credentials for this profile will be re-written.'.format(profile)
    else:
        profile = args.profile
        print 'Using "{0}" profile. Note: any existing credentials for this profile will be re-written.'.format(profile)
    print '-------------------------------------------------------------------------------------------------------------\n'
    if (not args.action or args.action =='login'):
        login(profile)
    elif(args.action and args.action =='logout'):
        logout(profile)
        
 
if __name__ == '__main__':
    main()