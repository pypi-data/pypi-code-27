import getpass
import boto3
from boto3.s3.transfer import S3Transfer
import os
import uuid
import requests
from tqdm import tqdm


MRIDATA_ORG = 'http://mridata.org/'


def download(uuid):
    r = requests.get(urljoin(MRIDATA_ORG, 'download/{}'.format(uuid)), stream=True)
    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024
    total_chunks = (total_size + chunk_size - 1) // chunk_size
    print('Downloading {}...'.format(uuid))
    with open('{}.h5'.format(uuid), 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), total=total_chunks, unit='KB'):
            if chunk:
                f.write(chunk)


def batch_download(filename):
    uuids = open(filename).read().splitlines()
    for uuid in uuids:
        download(uuid)
