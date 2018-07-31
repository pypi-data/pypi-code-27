import argparse
import hashlib
import os
import boto3
import botocore
import time
import datetime
import logging
import requests




session = boto3.Session(profile_name='test')
s3res = session.resource('s3')
s3client = session.client('s3')



def hashfunc(input):
    return hashlib.sha256('{}'.format(input).encode('utf-8')).hexdigest()

# Requirements for OS implemention to work:
# 1. Have clamav installed
# 2. run 'cp freshclam.conf.sample freshclam.conf' on command line ,
# 3. run freshclam, remove "example" from freshclam.conf

# Requirements for clamd implementation to work:
# 1. Everything in OS, but add '&& cp clamd.conf.sample clamd.conf' to step 2.
# 2. Remove "example" from clamd.conf also
# 3. Must change local socket section in clamd.conf to '/var/run/clamav/clamd.ctl'
def runscan(file):
    # Install clamav
    # Create config file with removal, remove stuff, change location in config for location, run daemon, etc.
    # Link: https://gist.github.com/mendozao/3ea393b91f23a813650baab9964425b9
    # Ask Chewy if there is a way for us to get an update
    os.system('clamscan {} -o --no-summary'.format(file))


def uploadDirectory(path, bucketname, key):
    for root, dirs, files in os.walk(path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, path)
            s3_path = os.path.join(key, relative_path)
            if file != '.DS_Store':
                # runscan(local_path)
                s3client.upload_file(local_path, bucketname, s3_path)


def logdata(action, filename, storedusername):
    timeatuse = time.time()
    formattedtime = datetime.datetime.fromtimestamp(timeatuse).strftime('%Y-%m-%d %H:%M:%S')
    action = action
    loggingdata = {'user': storedusername, 'date&time': formattedtime, 'filename': filename[1:], 'action': action}
    logging.info("I am now printing the log data: ")
    logging.info(loggingdata)
    logging.info('\n')
    return loggingdata


def sendloggingrequest(url, action, filename, user):
        return requests.post(url, data=logdata(action, filename, user), allow_redirects=False)


def runparser(user):
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()

    accolade_group = subparser.add_parser('storage')
    accolade_subparser2 = accolade_group.add_subparsers()

    accolade_remove = accolade_subparser2.add_parser('remove')
    accolade_remove.set_defaults(which='remove')
    accolade_remove.add_argument('rkey', help="Key within bucket to remove file")

    accolade_upload = accolade_subparser2.add_parser('upload')
    accolade_upload.set_defaults(which='upload')
    accolade_upload.add_argument('file', help="File that will be upload into the bucket-key location")
    accolade_upload.add_argument('--replace', help="Include on command line if replacing another file",
                                 action='store_true')

    accolade_dirupload = accolade_subparser2.add_parser('dirupload')
    accolade_dirupload.set_defaults(which='dirupload')
    accolade_dirupload.add_argument('directory', help="Absolute path to the directory that will be copied")
    args = vars(parser.parse_args())
    which = args['which']
    username = hashfunc(user)

    if which == 'dirupload':
        filename = args['directory']
        uploadDirectory(args['directory'], 'accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username)

    if which == 'upload':
        filename = '/' + args['file'].split('/')[-1]
        if args['replace']:
            try:
                s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + filename).load()
                print("going to replace now!")
                s3res.Object('accolade-platform-ext-dev-partners-577121982548',
                             'Hashed/' + username + filename).delete()
                runscan(args['file'])
                s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                     'Hashed/' + username + filename)
            except botocore.exceptions.ClientError:
                # For now pretending that accolade-platform-ext-dev-partners-577121982548 is makeup bucket
                print("Going into makeup bucket")
                runscan(args['file'])
                s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                     'Hashed/' + username + filename)
        else:
            runscan(args['file'])
            s3client.upload_file(args['file'], 'accolade-platform-ext-dev-partners-577121982548',
                                 'Hashed/' + username + filename)

    elif which == 'remove':
        filename = '/' + args['rkey']
        s3res.Object('accolade-platform-ext-dev-partners-577121982548', 'Hashed/' + username + filename).delete()

    logdata(which, filename, user)
    # sendloggingrequest(filename, which, filename, user)

